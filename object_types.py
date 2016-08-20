#-*- coding: utf-8 -*-

from utils import SlotDefinedClass


class Type(SlotDefinedClass):
    __slots__ = ("name", )


class FunctionType(Type):
    __slots__ = ("name", "return_type", "args")

    def __init__(self, **kwargs):
        kwargs = {k:str(v) for k,v in kwargs.iteritems()}
        super(FunctionType, self).__init__(**kwargs)


class FunctionDefinition(Type):
    __slots__ = FunctionType.__slots__ + ("body", )

    @classmethod
    def from_type(cls, func_type, body):
        assert isinstance(func_type, FunctionType)
        return FunctionDefinition(body=body, **func_type.json())


class FunctionCall(FunctionType):
    @classmethod
    def from_type(cls, func_type, args):
        assert isinstance(func_type, FunctionType)
        return FunctionCall(name=func_type.name,
                            return_type=func_type.return_type,
                            args=args)


class Module(Type):
    __slots__ = Type.__slots__ + ("body", )

