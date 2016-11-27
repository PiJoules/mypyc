# -*- coding: utf-8 -*-

import cgen

from builtin_types import *


class Value(cgen.Value):
    def get_decl_pair(self):
        return [str(self.typename)], self.name


class Assign(cgen.Generable):
    def __init__(self, var_type, var_name, rhs_type, rhs,
                 with_semicolon=False, op="=", previously_declared=False):
        self.__var_name = var_name
        self.__rhs_type = rhs_type
        self.__rhs = rhs
        self.__with_semicolon = with_semicolon
        self.__op = op
        self.__previously_declared = previously_declared
        self.__var_type = var_type

    def generate(self):
        previously_declared = self.__previously_declared
        var_type = self.__var_type
        op = self.__op

        if var_type.num_types() == 1:
            line = "{var_name} {op} {rhs}{last}"
            if not previously_declared:
                line = "{var_type} " + line
            line = line.format(
                var_type=self.__var_type,
                var_name=self.__var_name,
                op=op,
                rhs=self.__rhs,
                last=(";" if self.__with_semicolon else "")
            )
            yield line
        else:
            if op != "=":
                raise NotImplementedError("Implement calling of magic methods for augmented assignments.")

            line = """{var_name} = ({var_type}){{
    {enum_type},
    .{attr}={rhs}
}}{last}
            """
            if not previously_declared:
                line = "{var_type} " + line
            line = line.format(
                var_type=var_type,
                var_name=self.__var_name,
                enum_type=var_type.enum_type(self.__rhs_type),
                attr=var_type.attr_name(self.__rhs_type),
                rhs=self.__rhs,
                last=(";" if self.__with_semicolon else ""),
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


