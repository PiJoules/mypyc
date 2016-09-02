#-*- coding: utf-8 -*-

from utils import SlotDefinedClass


# Constants
MACRO_START = "#"
COLON = ":"
NEWLINE = "\n"
SPACE = " "
L_PAREN = "("
R_PAREN = ")"
DASH = "-"
G_THAN = ">"
UNDERSCORE = "_"
ASTERISK = "*"
COMMA = ","
D_QUOTE = "\""
BACKSLASH = "\\"
PERIOD = "."


# Keywords
DEFINITION = "def"
RETURN = "return"

KEYWORDS = set([
    DEFINITION,
    RETURN,
])


class Rule(SlotDefinedClass):
    pass


class Statement(Rule):
    pass


class Expression(Rule):
    pass


class Literal(Expression):
    pass


class NumberLiteral(Literal):
    pass


class WholeNumberLiteral(NumberLiteral):
    __types__ = ((int, long), )
    __slots__ = ("value", )


class DecimalNumberLiteral(NumberLiteral):
    pass


class StringLiteral(Literal):
    __types__ = (str, )
    __slots__ = ("value", )


class Module(Statement):
    __types__ = (str, [Statement])
    __slots__ = ("name", "body")


class Macro(Statement):
    __types__ = (str, )
    __slots__ = ("line", )


class FunctionArgument(Rule):
    __types__ = (str, str)
    __slots__ = ("name", "type")


class FunctionDefinition(Statement):
    __types__ = (str, [FunctionArgument], str, [Statement])
    __slots__ = ("name", "args", "return_type", "body")


class FunctionCall(Statement):
    __types__ = (str, [Expression])
    __slots__ = ("name", "args")


class ReturnStatement(Statement):
    __types__ = (Expression, )
    __slots__ = ("return_value", )


class Parser(object):
    def __init__(self, filename, indent_count=4):
        """
        Args:
            indent_count [int]: Number of spaces in an indentation.
        """
        self.__filename = filename
        self.__indent_count = indent_count
        self.__generator = self.char_generator()
        self.__line_no = 1
        self.__col_no = 1
        self.__char_buffer = ""  # Buffer used for peeking tokens
        self.pop_without_increment()

    def char_generator(self):
        with open(self.__filename, "r") as f:
            for line in f:
                for c in line:
                    yield c

    def next_char(self):
        """Pop the next char."""
        if self.__char_buffer:
            c = self.__char_buffer[0]
            self.__char_buffer = self.__char_buffer[1:]
            return c
        return next(self.__generator, "")

    def add_to_buffer(self, n=100):
        """
        Add up to n characters from the file.
        Returns the number of characters added.
        """
        for i in xrange(n):
            c = next(self.__generator, "")
            if c:
                self.__char_buffer += c
            else:
                return i
        return n

    def pop_without_increment(self):
        self.__token = self.next_char()

    def pop_token(self):
        if self.__token == NEWLINE:
            self.__col_no = 1
            self.__line_no += 1
        else:
            self.__col_no += 1
        self.pop_without_increment()

    def check_token(self, expect):
        assert self.__token == expect, "Expected '{}' on line {}, column {}. Found '{}'.".format(expect if expect != NEWLINE else "newline", self.__line_no, self.__col_no, self.__token)
        self.pop_token()

    def check_symbol(self, expect):
        tokens = ""
        for i in xrange(len(expect)):
            tokens += self.__token
            self.pop_token()
        assert tokens == expect, "Expected '{}' on line {}, column {}. Found '{}'.".format(expect, self.__line_no, self.__col_no, tokens)

    def check_right_arrow(self):
        """Check that we found a left arrow."""
        self.check_token(DASH)
        self.check_token(G_THAN)

    def skip_tokens(self, token):
        while self.__token == token:
            self.pop_token()

    def skip_spaces(self):
        """Ignore spaces. At least 1 must be given."""
        self.skip_tokens(SPACE)

    def skip_newlines(self):
        self.skip_tokens(NEWLINE)

    def check_indentation_level(self, expected_level):
        for i in xrange(expected_level * self.__indent_count):
            self.check_token(SPACE)

    def peek_symbols(self, n):
        """
        Peek n items off the buffer, combining characters that could be
        identifiers.
        """
        old_token = self.__token
        words = []
        word = ""
        buff = ""  # Characters read over to store on the buffer
        while len(words) < n and self.__token:
            if self.__token.isalnum() or self.__token == UNDERSCORE:
                word += self.__token
            else:
                if word:
                    words.append(word)
                    word = ""
                if not self.__token.isspace():
                    words.append(self.__token)
            buff += self.__token
            self.pop_without_increment()

        # Reset buffer and token
        if buff:
            self.__char_buffer = buff[1:] + self.__token + self.__char_buffer
        self.__token = old_token
        return words[:n]

    def peek_spaces(self):
        """Peek at the next sequence of spaces."""
        old_token = self.__token
        buff = ""
        while self.__token == SPACE and self.__token:
            buff += self.__token
            self.pop_without_increment()

        if buff:
            self.__char_buffer = buff[1:] + self.__token + self.__char_buffer
        self.__token = old_token
        return buff


    """
    Production Rules
    """

    def identifier(self):
        """
        Valid identifiers are alphanumeric characters or underscores, but
        must start with an alphabetic character.
        """
        if not self.__token.isalpha():
            raise RuntimeError("Expected alphabetic character for start of identifier on line {}, column {}.".format(self.__line_no, self.__col_no))
        word = self.__token
        self.pop_token()
        while self.__token.isalnum() or self.__token == UNDERSCORE:
            word += self.__token
            self.pop_token()
        return word

    def type(self):
        """Types consist of an identifier followed by optional *s for pointers."""
        name = self.identifier()
        while self.__token == ASTERISK:
            name += self.__token
            self.pop_token()
        return name

    def line(self):
        """
        Gets characters up to the first newline. The token at the end of this
        function call will be a newline character.
        """
        line = ""
        while self.__token != NEWLINE:
            line += self.__token
            self.pop_token()
        return line

    def macro(self):
        """
        1 line macros supported only for now.
        Just copy until the first newline.
        TODO: Add support for multiline macros.
        """
        line = self.line()
        return Macro(line=line)

    def function_argument(self):
        arg_name = self.identifier()
        self.skip_spaces()
        self.check_token(COLON)
        self.skip_spaces()
        arg_type = self.type()
        return FunctionArgument(
            name=arg_name,
            type=arg_type
        )

    def function_arguments_list(self):
        args = []
        while self.__token != R_PAREN:
            self.skip_spaces()

            if self.__token == COMMA:
                self.check_token(COMMA)
                continue

            arg = self.function_argument()
            args.append(arg)
        return args

    def function_definition(self, indent_level):
        self.check_symbol(DEFINITION)
        self.check_token(SPACE)
        self.skip_spaces()

        # Function name
        func_name = self.identifier()

        self.skip_spaces()
        self.check_token(L_PAREN)

        # Parse function args
        args = self.function_arguments_list()

        self.check_token(R_PAREN)
        self.skip_spaces()
        self.check_right_arrow()
        self.skip_spaces()

        # Return type
        return_type = self.type()

        self.check_token(COLON)
        self.check_token(NEWLINE)

        # Parse body
        body = self.statement_list(indent_level + 1)

        return FunctionDefinition(
            name=func_name,
            args=args,
            return_type=return_type,
            body=body
        )

    def string_literal(self):
        self.check_token(D_QUOTE)
        str_literal = ""
        while self.__token:
            if self.__token == D_QUOTE:
                # End of string literal
                self.check_token(D_QUOTE)
                break
            elif self.__token == BACKSLASH:
                # Escaped next character
                str_literal += self.__token
                self.pop_token()
                str_literal += self.__token
                self.pop_token()
            else:
                # Regular word
                str_literal += self.__token
                self.pop_token()
        return StringLiteral(value=str_literal)

    def number_literal(self):
        """
        Construct either whole number or decimal.
        TODO: Add support for numbers in other bases.
        """
        number = ""
        while self.__token.isdigit():
            number += self.__token
            self.pop_token()

        if self.__token == PERIOD:
            number += self.__token
            self.check_token(PERIOD)
            while self.__token.isdigit():
                number += self.__token
                self.pop_token()
            return DecimalNumberLiteral(value=float(number))

        return WholeNumberLiteral(value=int(number))

    def expression(self):
        """Handle different types of expressions."""
        token = self.__token
        if token == D_QUOTE:
            return self.string_literal()

        if token.isdigit():
            return self.number_literal()

        raise RuntimeError("Unknown token in expression '{}' on line {}, col {}.".format(token, self.__line_no, self.__col_no))

    def expression_list(self):
        args = []
        while self.__token != R_PAREN:
            self.skip_spaces()

            if self.__token == COMMA:
                self.check_token(COMMA)
                continue

            arg = self.expression()
            args.append(arg)
        return args

    def function_call(self):
        func_name = self.identifier()

        self.check_token(L_PAREN)

        # Parse function arguments
        exprs = self.expression_list()

        self.check_token(R_PAREN)
        return FunctionCall(
            name=func_name,
            args=exprs
        )

    def return_statement(self):
        self.check_symbol(RETURN)
        self.check_token(SPACE)
        self.skip_spaces()
        return ReturnStatement(return_value=self.expression())

    def statement(self, indent_level):
        token = self.__token
        if token == MACRO_START:
            return self.macro()

        symbol, lookahead = self.peek_symbols(2)
        if symbol == DEFINITION:
            return self.function_definition(indent_level)
        elif symbol == RETURN:
            return self.return_statement()
        elif lookahead == L_PAREN:
            return self.function_call()

        raise RuntimeError("Unknown symbol '{}' on line {}, col {}.".format(symbol, self.__line_no, self.__col_no))

    def statement_list(self, indent_level):
        """
        Leave the statement list once we find an indentation level less than
        this one.
        """
        body = []
        expected_indentation = indent_level * self.__indent_count
        self.skip_newlines()
        while self.__token:

            # We have finished 1 scope if we find that the line starts with
            # the same indent level as expected.
            indentation = self.peek_spaces()
            if len(indentation) % self.__indent_count:
                raise RuntimeError("Impropert indentation on line {}, col {}. Indentations must be a multiple of {} spaces.".format(self.__line_no, self.__col_no, self.__indent_count))
            elif len(indentation) < expected_indentation:
                return body
            elif len(indentation) > expected_indentation:
                raise RuntimeError("More indentaitons found than expected on line {}, col {}. {} were expected. {} were found.".format(self.__line_no, self.__col_no, indent_level, len(indentation) / self.__indent_count))

            # In same scope, proceed normally.
            self.skip_spaces()
            body.append(self.statement(indent_level))

            if self.__token:
                self.check_token(NEWLINE)
                self.skip_newlines()
        return body

    def module(self, module_name):
        return Module(
            name=module_name,
            body=self.statement_list(0)
        )

    def parse(self):
        return self.module("__main__")

