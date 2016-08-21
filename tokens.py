#-*- coding: utf-8 -*-

__all__ = ("StringToken", "Word", "Indentation", "Newline", "Symbol",
           "WholeNumber", "DecimalNumber")

from utils import SlotDefinedClass, contains_whitespace


class Token(SlotDefinedClass):
    pass


class StringToken(Token):
    """Series of characters."""
    __types__ = (str, )
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
    __types__ = StringToken.__types__
    __slots__ = StringToken.__slots__

    """Series of non-whitespace characters."""
    def __init__(self, **kwargs):
        assert not contains_whitespace(kwargs["chars"])
        super(Word, self).__init__(**kwargs)


class Indentation(Token):
    __types__ = (int, )
    __slots__ = ("size", )

    def __repr__(self):
        return "<Indentation (size={})>".format(self.size)

    def __eq__(self, other):
        if not isinstance(other, Indentation):
            return False
        return self.size == other.size

    @classmethod
    def check_indentation(cls, ind, size=None):
        assert isinstance(ind, Indentation)
        if size is not None:
            assert ind.size == size

    def __str__(self):
        return " " * self.size


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
    __types__ = (str, )
    __slots__ = ("char", )

    def __repr__(self):
        return "<Symbol ('{}')>".format(self.char)

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.char
        if not isinstance(other, Symbol):
            return False
        return self.char == other.char

    @classmethod
    def check_symbol(cls, symbol, char=None):
        assert isinstance(symbol, Symbol)
        if char:
            assert symbol.char == char

    def __str__(self):
        return self.char


class Number(Token):
    __types__ = (int, )
    __slots__ = ("value", )

    def __repr__(self):
        return "<{} ({})>".format(type(self).__name__, self.value)

    def __eq__(self, other):
        if isinstance(other, (int, long, float)):
            return self.value == other
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value

    def __str__(self):
        return str(self.value)


class WholeNumber(Number):
    __types__ = (int, )
    __slots__ = ("value", )


class DecimalNumber(Number):
    __types__ = (float, )
    __slots__ = ("value", )

