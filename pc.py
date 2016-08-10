#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lexer import Lexer, Word, Indentation, Newline, Symbol

import sys


class Rule(object):
    pass


class Parser(object):
    """Class for creating the parse tree."""

    def __init__(self, tokens):
        assert tokens
        self.__tokens = tokens

    def parse(self):
        tokens = self.__tokens
        token = tokens.pop(0)

        assert isinstance(token, Word)
        assert token.chars() == "def"

        while tokens:
            if isinstance(token, Word) and token.chars() == "def":
                self.parse_def()

            token = tokens.pop(0)

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
        while tokens[-1] == "*":
            count += 1
        full_type = Word(type_name.chars() + "*"*count)

        return full_type

    def parse_args(self):
        tokens = self.__tokens
        token = tokens.pop(0)
        while token != ")":
            # Argument name
            Word.check_word(token)
            arg_name = token

            Symbol.check_symbol(tokens.pop(0), ":")

            # Argument type
            arg_type = self.parse_type()
            print(arg_type)

            token = tokens.pop(0)

    def parse_def(self):
        """Parse function definition."""
        tokens = self.__tokens

        # Get function name
        token = tokens.pop(0)
        assert isinstance(token, Word)
        func_name = token

        # Check parentheses
        Symbol.check_symbol(tokens.pop(0), "(")

        # Get args
        self.parse_args()


def main():
    filename = sys.argv[1]
    lexer = Lexer(filename)
    tokens = [token for token in lexer]
    for token in tokens:
        print("'{}'".format(token))

    parser = Parser(tokens)
    parser.parse()

    return 0


if __name__ == "__main__":
    main()

