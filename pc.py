#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys


class Rule(object):
    pass


class Token(object):
    pass


class Word(Token):
    def __init__(self, chars):
        self.__chars = chars

    def __repr__(self):
        return "<Word ({})>".format(self.__chars)


class Indentation(Token):
    def __init__(self, size):
        self.__size = 4

    def __repr__(self):
        return "<Indentation (size={})>".format(self.__size)


class Newline(Token):
    pass


class NoMoreLinesException(Exception):
    """No more lines are available in the file."""
    pass


class Lexer(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__file = open(filename, "r")
        self.__buffer = []

    def has_next(self):
        """
        Check if there are any more tokens that can be popped.
        Automatically adds tokens if buffer is empty.
        """
        if self.__buffer:
            return True

        try:
            self.__add_tokens()
        except NoMoreLinesException:
            return False
        return True

    def __tokenize_line(self, line):
        """Split a line into tokens"""
        tokens = [""]
        last_idx = 0

        for c in line:
            if c.isalnum():
                # Add new char to last buffer
                tokens[last_idx] += c
            else:
                # Whitespace or other
                if not tokens[last_idx]:
                    tokens[last_idx] = c
                else:
                    tokens.append(c)
                    last_idx += 1
                tokens.append("")
                last_idx += 1

        if not tokens[last_idx]:
            tokens = tokens[:-1]

        return tokens

    def __add_tokens(self):
        """Add tokens from the file to the buffer."""
        try:
            line = next(self.__file)
        except StopIteration:
            raise NoMoreLinesException()

        # Split the line by whitespace
        tokens = self.__tokenize_line(line)
        if tokens:
            self.__buffer += tokens
        else:
            raise NoMoreLinesException()

    def next(self):
        """Pop a token from the buffer."""
        return self.__buffer.pop(0)

    def __iter__(self):
        while self.has_next():
            yield self.next()


def main():
    lexer = Lexer(sys.argv[1])
    for token in lexer:
        print("'" + token + "'")

    return 0


if __name__ == "__main__":
    main()

