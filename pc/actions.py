#-*- coding: utf-8 -*-

__all__ = ("Action", "Declaration", "FunctionDeclaration", "FunctionCall",
           "FunctionDefinition", "VariableDeclaration", "Return")

from utils import SlotDefinedClass
from object_types import Type
from literals import Literal


class Action(SlotDefinedClass):
    __slots__ = ()


class Declaration(Action):
    """
    Contains information about variables available in a frame.
    - value type for variables
    - return type + args and their types for functions
    """
    __types__ = (str, )
    __slots__ = ("name", )


class FunctionDeclaration(Declaration):
    __types__ = Declaration.__types__ + (Type, list)
    __slots__ = Declaration.__slots__ + ("return_type", "arg_types")


class FunctionCall(Action):
    __types__ = (list, Declaration)
    __slots__ = ("args", "declaration")

    @classmethod
    def from_declaration(cls, declaration, args):
        assert isinstance(declaration, FunctionDeclaration)
        return cls(args=args, declaration=declaration)


class FunctionDefinition(Action):
    """Define an laready declared function or declare and define a new one."""
    __types__ = (str, Type, list, list)
    __slots__ = ("name", "return_type", "arg_types", "body")

    @classmethod
    def from_declaration(cls, declaration, body):
        assert isinstance(declaration, FunctionDeclaration)
        return cls(body=body, **declaration.dict())


class VariableDeclaration(Declaration):
    __types__ = Declaration.__types__ + (Type, )
    __slots__ = Declaration.__slots__ + ("type", )


class Return(Action):
    __types__ = ((Literal, Declaration), )
    __slots__ = ("decl", )


