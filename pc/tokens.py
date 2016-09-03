# -*- coding: utf-8 -*-

"""
Tokens will be a close 1 to 1 copy of the original code where each token was
separated by whitespace. Just need a well-enough defined method of being able
to tell apart words, symbols, indentations, and numbers from each other
without having to worry about delimiting whitespace.
"""

from utils import SlotDefinedClass
from symbols import *


class Token(SlotDefinedClass):
    __types__ = (int, int, str)
    __slots__ = ("line_no", "col_no", "value")

    def __str__(self):
        return "<{cls_name} line_no={line_no} col_no={col_no} value='{value}'>".format(
            cls_name=type(self).__name__,
            line_no=self.line_no,
            col_no=self.col_no,
            value=self.value
        )

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def check(cls, token, value=None):
        assert isinstance(token, cls), "Expected a '{}' on line {}, col {}. Found {}".format(cls.__name__, token.line_no, token.col_no, token)
        if value is not None:
            assert value == token.value, "Expected value '{}' on line {}, col {}. Found {}".format(value, token.line_no, token.col_no, token.value)


class Word(Token):
    pass


class Symbol(Token):
    pass


class Newline(Token):
    @classmethod
    def from_location(cls, line_no, col_no):
        return cls(
            line_no=line_no,
            col_no=col_no,
            value=NEWLINE
        )

    def __str__(self):
        return "<{cls_name} line_no={line_no} col_no={col_no}>".format(
            cls_name=type(self).__name__,
            line_no=self.line_no,
            col_no=self.col_no
        )


class Number(Token):
    pass


class Indent(Token):
    @classmethod
    def from_size(cls, line_no, col_no, size):
        return cls(
            line_no=line_no,
            col_no=col_no,
            value=SPACE * size
        )

    def __str__(self):
        return "<{cls_name} line_no={line_no} col_no={col_no} size={size}>".format(
            cls_name=type(self).__name__,
            line_no=self.line_no,
            col_no=self.col_no,
            size=len(self.value)
        )


class Quote(Token):
    pass


