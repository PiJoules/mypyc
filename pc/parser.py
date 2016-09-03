#-*- coding: utf-8 -*-

from symbols import *
from rules import *
from tokens import *
from lexer import Lexer


# Keywords
DEFINITION = "def"
RETURN = "return"

KEYWORDS = set([
    DEFINITION,
    RETURN,
])


class Parser(object):
    def __init__(self, filename, indent_count=4):
        """
        Args:
            indent_count [int]: Number of spaces in an indentation.
        """
        self.__indent_count = indent_count
        self.__token_buffer = []  # Buffer used for peeking tokens
        self.__lexer = Lexer(filename, indent_count=indent_count)
        self.__pop_token()

    def __pop_token(self):
        if self.__token_buffer:
            self.__token = self.__token_buffer.pop(0)
            return
        self.__token = self.__lexer.next_token()


    """
    Token checks
    """

    def __check_token(self, token_type, value=None):
        token_type.check(self.__token, value=value)
        self.__pop_token()

    def __check_word(self, expect=None):
        self.__check_token(Word, value=expect)

    def __check_symbol(self, expect):
        self.__check_token(Symbol, value=expect)

    def __check_newline(self):
        self.__check_token(Newline)

    def __check_number(self):
        self.__check_token(Number)

    def __check_indent(self):
        self.__check_token(Indent, value=SPACE * self.__indent_count)

    def __check_quote(self):
        self.__check_token(Quote)



    def __check_right_arrow(self):
        """Check that we found a left arrow."""
        self.__check_symbol(DASH)
        self.__check_symbol(G_THAN)

    def __peek_tokens(self, n):
        """
        Peek n items off the buffer, combining characters that could be
        identifiers.
        """
        if n <= 0:
            return []
        old_token = self.__token
        tokens = [self.__token]
        for i in xrange(n-1):
            self.__pop_token()
            tokens.append(self.__token)

        # Reset buffer and token
        self.__token_buffer = tokens[1:] + self.__token_buffer
        self.__token = old_token
        return tokens


    """
    Production Rules
    """

    def identifier(self):
        """
        Valid identifiers are alphanumeric characters or underscores, but
        must start with an alphabetic character.
        """
        token = self.__token
        if not token.value[0].isalpha():
            raise RuntimeError("Expected alphabetic character for start of identifier on line {}, column {}. Found {}.".format(token.line_no, token.col_no, token))
        self.__pop_token()
        return token.value

    def type(self):
        """Types consist of an identifier followed by optional *s for pointers."""
        name = self.identifier()
        while self.__token == ASTERISK:
            name += self.__token.value
            self.__pop_token()
        return name

    def macro(self):
        """
        1 line macros supported only for now.
        Just copy until the first newline.
        TODO: Add support for multiline macros.
        """
        self.__check_symbol(MACRO_START)
        line = MACRO_START
        while self.__token != NEWLINE:
            line += self.__token.value
            self.__pop_token()
        return Macro(line=line)

    def function_argument(self):
        arg_name = self.identifier()
        self.__check_symbol(COLON)
        arg_type = self.type()
        return FunctionArgument(
            name=arg_name,
            type=arg_type
        )

    def function_arguments_list(self):
        args = []
        while self.__token != R_PAREN:
            if self.__token == COMMA:
                self.__check_symbol(COMMA)
                continue
            arg = self.function_argument()
            args.append(arg)
        return args

    def function_definition(self, indent_level):
        self.__check_word(DEFINITION)

        # Function name
        func_name = self.identifier()

        self.__check_symbol(L_PAREN)

        # Parse function args
        args = self.function_arguments_list()

        self.__check_symbol(R_PAREN)
        self.__check_right_arrow()

        # Return type
        return_type = self.type()

        self.__check_symbol(COLON)
        self.__check_newline()

        # Parse body
        body = self.statement_list(indent_level + 1)

        return FunctionDefinition(
            name=func_name,
            args=args,
            return_type=return_type,
            body=body
        )

    def number_literal(self):
        """
        Construct either whole number or decimal.
        TODO: Add support for numbers in other bases.
        """
        number = self.__token.value
        self.__pop_token()

        if self.__token == PERIOD:
            number += PERIOD
            self.__pop_token()
            number += self.__token.value
            self.__pop_token()
            return DecimalNumberLiteral(value=float(number))

        return WholeNumberLiteral(value=int(number))

    def expression(self):
        """Handle different types of expressions."""
        token = self.__token
        if isinstance(token, Quote):
            self.__pop_token()
            return StringLiteral(value=token.value)
        elif isinstance(token, Number):
            return self.number_literal()

        raise RuntimeError("Unknown token in expression '{}' on line {}, col {}.".format(token, token.line_no, token.col_no))

    def expression_list(self):
        args = []
        while self.__token != R_PAREN:
            if self.__token == COMMA:
                self.__check_symbol(COMMA)
                continue

            arg = self.expression()
            args.append(arg)
        return args

    def function_call(self):
        func_name = self.identifier()

        self.__check_symbol(L_PAREN)

        # Parse function arguments
        exprs = self.expression_list()

        self.__check_symbol(R_PAREN)
        return FunctionCall(
            name=func_name,
            args=exprs
        )

    def return_statement(self):
        self.__check_word(RETURN)
        return ReturnStatement(return_value=self.expression())

    def statement(self, indent_level):
        token = self.__token
        if token == MACRO_START:
            return self.macro()

        symbol, lookahead = self.__peek_tokens(2)
        if symbol == DEFINITION:
            return self.function_definition(indent_level)
        elif symbol == RETURN:
            return self.return_statement()
        elif lookahead == L_PAREN:
            return self.function_call()

        raise RuntimeError("Unknown symbol '{}' on line {}, col {}.".format(symbol, symbol.line_no, symbol.col_no))

    def statement_list(self, indent_level):
        """
        Leave the statement list once we find an indentation level less than
        this one.
        """
        body = []
        while self.__token:
            # We have finished 1 scope if we find that the line starts with
            # smaller indent level as expected.
            for token in self.__peek_tokens(indent_level):
                if not isinstance(token, Indent):
                    return body

            # In same scope, proceed normally.
            for i in xrange(indent_level):
                self.__check_indent()
            body.append(self.statement(indent_level))

            if self.__token:
                self.__check_newline()
        return body

    def module(self, module_name):
        return Module(
            name=module_name,
            body=self.statement_list(0)
        )

    def parse(self):
        return self.module("__main__")

