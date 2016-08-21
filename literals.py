#-*- coding: utf-8 -*-

__all__ = ("Literal", "StringLiteral", "IntegerLiteral")

from utils import SlotDefinedClass
from tokens import *
from object_types import *


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

    def __str__(self):
        return self.chars


class IntegerLiteral(Literal):
    __types__ = (IntegerType, int)
    __slots__ = Literal.__slots__ + ("value", )

    @classmethod
    def from_token(cls, token):
        assert isinstance(token, WholeNumber)
        return cls(value=token.value, type=IntegerType())

    def __str__(self):
        return str(self.value)

