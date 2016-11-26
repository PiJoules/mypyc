# -*- coding: utf-8 -*-

import cgen

from builtin_types import *


class Value(cgen.Value):
    def get_decl_pair(self):
        return [str(self.typename)], self.name


class Assign(cgen.Generable):
    def __init__(self, var_name, rhs, with_semicolon=False, op="=",
                 var_type=None):
        self.__var_name = var_name
        self.__rhs = rhs
        self.__with_semicolon = with_semicolon
        self.__op = op
        self.__var_type = var_type

    def generate(self):
        line = "{var_name} {op} {rhs}{last}"
        if self.__var_type is not None:
            line = "{var_type} " + line
        line = line.format(
            var_type=self.__var_type,
            var_name=self.__var_name,
            op=self.__op,
            rhs=self.__rhs,
            last=(";" if self.__with_semicolon else "")
        )
        yield line

