#-*- coding: utf-8 -*-

from utils import SlotDefinedClass
from lexer import StringToken
from object_types import Type, StringType


class Literal(SlotDefinedClass):
    __types__ = (Type, )
    __slots__ = ("type", )


class StringLiteral(Literal):
    __types__ = (StringType, str)
    __slots__ = Literal.__slots__ + ("chars", )

    @classmethod
    def from_token(cls, str_token):
        assert isinstance(str_token, StringToken)
        return cls(chars=str_token.chars, type=StringType())
