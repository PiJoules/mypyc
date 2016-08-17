#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lexer import Lexer, Word, Indentation, Newline, Symbol

import sys


BASE_INDENTATION_SIZE = 4


class SlotDefinedClass(object):
    __slots__ = tuple()

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs[attr])

    def __str__(self):
        return str({k:getattr(self, k) for k in self.__slots__})


class Variable(SlotDefinedClass):
    __slots__ = ("name", )


class Function(Variable):
    __slots__ = ("name", "return_type", "args")

    def __init__(self, **kwargs):
        assert isinstance(kwargs["name"], Word)
        assert isinstance(kwargs["return_type"], Word)
        assert isinstance(kwargs["args"], list)
        super(Function, self).__init__(**kwargs)

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        return self.name == other.name


class Frame(object):
    def __init__(self, variables=None):
        variables = variables or []
        assert all(isinstance(v, Variable) for v in variables)
        self.__variables = variables

    def variables(self):
        return self.__variables

    def append(self, item):
        self.__variables.append(item)

    def __add__(self, item):
        if isinstance(item, list):
            vars = item
        elif isinstance(item, Frame):
            vars = item.variables()
        return Frame(variables=self.variables() + vars)

    def __contains__(self, item):

        if isinstance(item, (str, Word)):
            return self.name == other
        return self.name == other.name

    def __iter__(self):
        return iter(self.__variables)


def load_global_frame():
    printf_func = Function(name=Word("printf"), return_type=Word("void"), args=[])
    return Frame([printf_func])


class Parser(object):
    """Class for creating the parse tree."""

    def __init__(self, tokens):
        assert tokens
        self.__tokens = tokens
        self.__global_frame = load_global_frame()

    def parse_module(self, indentation_level):
        tokens = self.__tokens
        token = tokens.pop(0)

        assert isinstance(token, Word)
        assert token.chars() == "def"

        global_frame = self.__global_frame

        while tokens:
            if isinstance(token, Word) and token.chars() == "def":
                self.parse_def(indentation_level, global_frame)

            token = tokens.pop(0)

    def parse(self):
        """When parsing a regular file, just parsing a module."""
        return self.parse_module(0)

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
        full_type = Word(type_name.chars() + "*"*count)

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

    def parse_body(self, indentation_level, frame):
        """Parse a body of a new frame."""
        tokens = self.__tokens
        word = tokens.pop(0)
        Word.check_word(word)
        print(word)
        print(map(str, frame))
        print(word in frame)

        # This word can be (for now) a:
        # - Function call
        # - Variable definition
        # - Function definition
        if word == "def":
            func = self.parse_def(indentation_level)
        elif word in frame:
            pass
        else:
            raise RuntimeError("Unknown word: {}".format(word))

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
        func = Function(name=func_name, return_type=return_type, args=args)

        # Parse body of def
        body = self.parse_body(indentation_level, frame + [func])

def main():
    filename = sys.argv[1]
    lexer = Lexer(filename)
    tokens = [token for token in lexer]

    print("Tokens")
    for token in tokens:
        print("'{}'".format(token))
    print("")

    parser = Parser(tokens)
    parser.parse()

    return 0


if __name__ == "__main__":
    main()

