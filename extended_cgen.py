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


class AssignMultipleType(Assign):
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


class Grouping(cgen.Generable):
    GROUPING_NAME = NotImplemented
    SEPARATPOR = NotImplemented

    def __init__(self, name, attributes, with_semicolon=False):
        self.__name = name
        self.__attrs = attributes
        self.__with_semicolon = with_semicolon

    def generate(self):
        yield """{grouping_name} {name} {{
    {attributes}
}}{last}
        """.format(
            grouping_name=self.GROUPING_NAME,
            name=self.__name,
            attributes="".join(
                ["    {line}{sep}\n".format(line=l, sep=self.SEPARATPOR)
                 for l in map(str, self.__attrs)]
            ),
            last=";" if self.__with_semicolon else ""
        )


class Enum(Grouping):
    GROUPING_NAME = "enum"
    SEPARATPOR = ","


class Struct(Grouping):
    GROUPING_NAME = "struct"
    SEPARATPOR = ";"


class Union(Grouping):
    GROUPING_NAME = "union"
    SEPARATPOR = ";"


