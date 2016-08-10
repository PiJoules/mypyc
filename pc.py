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
            token = tokens.pop(0)
            if isinstance(token, Word):
                self.parse_def()

    def parse_def(self):
        """Parse function definition."""
        tokens = self.__tokens
        token = tokens.pop(0)

        assert isinstance(token, Word)



def main():
    filename = sys.argv[1]
    lexer = Lexer(filename)
    for token in lexer:
        print("'{}'".format(token))

    return 0


if __name__ == "__main__":
    main()

