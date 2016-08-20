#-*- coding: utf-8 -*-

from utils import SlotDefinedClass, contains_whitespace


class Token(SlotDefinedClass):
    def __ne__(self, other):
        return not (self == other)


class StringToken(Token):
    """Series of characters."""
    __slots__ = ("chars", )

    def __repr__(self):
        return "<{} ({})>".format(type(self).__name__, self.chars)

    @classmethod
    def check_word(cls, word, chars=None):
        assert isinstance(word, cls)
        if chars:
            assert chars == word.chars

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.chars
        if not isinstance(other, type(self)):
            return False
        return other.chars == self.chars

    def __str__(self):
        return self.chars


class Word(StringToken):
    """Series of non-whitespace characters."""
    def __init__(self, **kwargs):
        assert not contains_whitespace(kwargs["chars"])
        super(Word, self).__init__(**kwargs)


class Indentation(Token):
    def __init__(self, size):
        self.__size = size

    def __repr__(self):
        return "<Indentation (size={})>".format(self.__size)

    def size(self):
        return self.__size

    def __eq__(self, other):
        if not isinstance(other, Indentation):
            return False
        return self.__size == other.size()

    @classmethod
    def check_indentation(cls, ind, size=None):
        assert isinstance(ind, Indentation)
        if size is not None:
            assert ind.size() == size

    def __str__(self):
        return " " * self.__size


class Newline(Token):
    def __repr__(self):
        return "<Newline>"

    def __eq__(self, other):
        return isinstance(other, Newline)

    @classmethod
    def check_newline(cls, symbol):
        assert isinstance(symbol, Newline)

    def __str__(self):
        return "\n"


class Symbol(Token):
    def __init__(self, char):
        self.__char = char

    def __repr__(self):
        return "<Symbol ('{}')>".format(self.__char)

    def char(self):
        return self.__char

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.__char
        if not isinstance(other, Symbol):
            return False
        return self.__char == other.char()

    @classmethod
    def check_symbol(cls, symbol, char=None):
        assert isinstance(symbol, Symbol)
        if char:
            assert symbol.char() == char

    def __str__(self):
        return self.__char
