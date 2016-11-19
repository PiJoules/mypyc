# -*- coding: utf-8 -*-

from value import *

import ast


class Function(object):
    def __init__(self, name, args, body, decorators):
        self.__name = name
        self.__args = args
        self.__body = body
        self.__decorators = decorators

        self.__arg_types = self.__evaluate_arg_types()
        self.__return_type = self.__evaluate_return_type()

    @classmethod
    def from_func_def_node(cls, node):
        return cls(node.name,
                   node.args,
                   node.body,
                   node.decorator_list)

    def __evaluate_return_type(self):
        """Find first return value, if none is found, return type is void."""
        for statement in self.__body:
            if isinstance(statement, ast.Return):
                return value_from_node(statement.value)
        return "void"

    def __evaluate_arg_types(self):
        """Find instances of operations where these values are used and
        determine type from operation."""
        types = []
        for arg in self.__args:
            for statement in self.__body:
                if isinstance(statement, ast.Assign):
                    targets = statement.targets
                    value = statement.value
        return types

    def return_type(self):
        return self.__return_type

    def name(self):
        return self.__name

    def body(self):
        return self.__body


