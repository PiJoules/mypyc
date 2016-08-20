#-*- coding: utf-8 -*-

from utils import SlotDefinedClass
from lexer import Word, Indentation, Newline, Symbol, StringToken
from object_types import (
    Type, FunctionType, FunctionDefinition, FunctionCall, Module
)

BASE_INDENTATION_SIZE = 4


class Frame(object):
    """Frame of variables available in the scope of a function."""
    def __init__(self, variables=None):
        variables = variables or []
        assert all(isinstance(v, Type) for v in variables)
        self.__variables = variables

    def variables(self):
        return self.__variables

    def get(self, name):
        return next(iter(v for v in self.__variables if v.name == name), None)

    def __add__(self, other):
        if isinstance(other, list):
            return Frame(self.__variables + other)
        return Frame(self.__variables + other.variables())

    def __iter__(self):
        return iter(self.__variables)

    def __contains__(self, item):
        if isinstance(item, Word):
            name = item.chars
        else:
            raise TypeError("Cannot check contains for type {}".format(item.__class__))
        return self.get(name)


def load_global_frame():
    """Create a frame of all the available functions."""
    printf_func = FunctionType(name="printf", return_type="void", args=[])
    return Frame([printf_func])


class Parser(object):
    """Class for creating the parse tree."""

    def __init__(self, tokens):
        assert tokens
        self.__tokens = tokens
        self.__global_frame = load_global_frame()

    def token_is_def(self, token):
        """Check if a token is a function definition."""
        return isinstance(token, Word) and token.chars == "def" and isinstance(self.__tokens[0], Word)

    def parse_module(self, indentation_level, module_name):
        """Parse a module."""
        tokens = self.__tokens
        token = tokens.pop(0)

        assert isinstance(token, Word)
        assert token.chars == "def"

        global_frame = self.__global_frame

        body = []
        while tokens:
            if self.token_is_def(token):
                func_def = self.parse_def(indentation_level, global_frame)
                body.append(func_def)
        return Module(body=body, name=module_name)

    def parse(self):
        """When parsing a regular file, just parsing a module."""
        return self.parse_module(0, "__main__")

    def parse_type(self):
        """
        Argument types (for now):
        - 1 word: int, long, char, etc.
        - 1 word followed by stars: int*, long**, char***, etc.
        """
        tokens = self.__tokens
        token = tokens.pop(0)

        # Word part
        Word.check_word(token)
        type_name = token

        # Stars
        count = 0
        while tokens[0] == "*":
            tokens.pop(0)
            count += 1
        full_type = type_name.chars + "*"*count

        return full_type

    def parse_def_args(self, indentation_level):
        """Parse definition arguments."""
        tokens = self.__tokens
        token = tokens.pop(0)

        args = []

        while token != ")":
            if token == ",":
                token = tokens.pop(0)

            # Argument name
            Word.check_word(token)
            arg_name = token

            Symbol.check_symbol(tokens.pop(0), ":")

            # Argument type
            arg_type = self.parse_type()
            args.append(arg_type)

            token = tokens.pop(0)

        Symbol.check_symbol(tokens.pop(0), "-")
        Symbol.check_symbol(tokens.pop(0), ">")

        return_type = self.parse_type()
        Symbol.check_symbol(tokens.pop(0), ":")
        Newline.check_newline(tokens.pop(0))
        return args, return_type

    def parse_func_call_args(self, variable, frame):
        tokens = self.__tokens
        Symbol.check_symbol(tokens.pop(0), "(")
        top = tokens[0]  # Peek only

        args = []

        while top != ")":
            if top == ",":
                tokens.pop(0)

            # Type or function evaluation
            arg = self.parse_variable(None, frame)
            args.append(arg)

            top = tokens[0]
        tokens.pop(0)

        return args

    def parse_variable(self, indentation_level, frame):
        """Parse a body of a new frame."""
        tokens = self.__tokens
        token = tokens.pop(0)

        if isinstance(token, Word):
            # This word can be (for now) a:
            # - Function call
            # - Function definition
            # - Type definition
            word = token
            variable = frame.get(word)
            if self.token_is_def(word):
                # Function definition
                func = self.parse_def(indentation_level, frame)
            elif variable:
                if isinstance(variable, FunctionType):
                    # Call the function
                    # Parse the arguments
                    args = self.parse_func_call_args(variable, frame)
                    return FunctionCall.from_type(variable, args)
                else:
                    # Calling a regular variable
                    raise RuntimeError("Type {} is not a function.".format(variable))
            else:
                raise RuntimeError("Unknown word: {}".format(word))
        elif isinstance(token, StringToken):
            return token
        else:
            raise RuntimeError("Unknown token type: {}".format(token))

    def parse_def(self, indentation_level, frame):
        """Parse function definition."""
        tokens = self.__tokens

        # Get function name
        token = tokens.pop(0)
        assert isinstance(token, Word)
        func_name = token

        # Check parentheses
        Symbol.check_symbol(tokens.pop(0), "(")

        # Get args
        args, return_type = self.parse_def_args(indentation_level)

        # Check indentation
        Indentation.check_indentation(tokens.pop(0), BASE_INDENTATION_SIZE + indentation_level)
        indentation_level += BASE_INDENTATION_SIZE

        # Declare function
        func = FunctionType(name=func_name, return_type=return_type, args=args)

        # Parse body of def
        actions = []
        action = self.parse_variable(indentation_level, frame + [func])
        actions.append(action)

        # Must be 1 newline
        Newline.check_newline(tokens.pop(0))
        while tokens:
            token = tokens.pop(0)

            # Any number of newlines can be followed
            if isinstance(token, Newline):
                continue

            # Indentation must be the same
            Indentation.check_indentation(tokens.pop(0), indentation_level)

            # Parse rest of body
            action = self.parse_variable(indentation_level, frame + [func])
            actions.append(action)
        return FunctionDefinition.from_type(func, actions)
