#-*- coding: utf-8 -*-

from utils import SlotDefinedClass


class Rule(SlotDefinedClass):
    pass


class Statement(Rule):
    pass


class Expression(Rule):
    pass


class Literal(Expression):
    pass


class NumberLiteral(Literal):
    pass


class WholeNumberLiteral(NumberLiteral):
    __types__ = ((int, long), )
    __slots__ = ("value", )


class DecimalNumberLiteral(NumberLiteral):
    pass


class StringLiteral(Literal):
    __types__ = (str, )
    __slots__ = ("value", )


class Module(Statement):
    __types__ = (str, [Statement])
    __slots__ = ("name", "body")


class Macro(Statement):
    __types__ = (str, )
    __slots__ = ("line", )


class FunctionArgument(Rule):
    __types__ = (str, str)
    __slots__ = ("name", "type")


class FunctionDefinition(Statement):
    __types__ = (str, [FunctionArgument], str, [Statement])
    __slots__ = ("name", "args", "return_type", "body")


class FunctionCall(Statement):
    __types__ = (str, [Expression])
    __slots__ = ("name", "args")


class ReturnStatement(Statement):
    __types__ = (Expression, )
    __slots__ = ("return_value", )


