#-*- coding: utf-8 -*-

from utils import SlotDefinedClass
from lexer import StringToken


class Literal(SlotDefinedClass):
    __slots__ = ()


class StringLiteral(Literal):
    __types__ = (str, )
    __slots__ = ("chars", )

    @classmethod
    def from_token(cls, str_token):
        assert isinstance(str_token, StringToken)
        return cls(chars=str_token.chars)
