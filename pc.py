#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lexer import Lexer, Word, Indentation, Newline, Symbol

import sys


BASE_INDENTATION_SIZE = 4


class Rule(object):
    pass


class Parser(object):
    """Class for creating the parse tree."""

    def __init__(self, tokens):
        assert tokens
        self.__tokens = tokens

    def parse_module(self, indentation_level):
        tokens = self.__tokens
        token = tokens.pop(0)

        assert isinstance(token, Word)
        assert token.chars() == "def"

        while tokens:
            if isinstance(token, Word) and token.chars() == "def":
                self.parse_def(indentation_level)

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

    def parse_body(self, indentation_level):
        """Parse a body of a new frame."""
        word = tokens.pop(0)
        Word.check_word(word)

        # This word can be (for now) a:
        # - Function call
        # - Variable declaration/definition

    def parse_def(self, indentation_level):
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

        # Parse body of def


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

