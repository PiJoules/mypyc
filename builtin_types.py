# -*- coding: utf-8 -*-

import cgen
import extended_cgen


class Type(object):
    def __init__(self, *names):
        self.__first_name = names[0]
        self.__names = set(names)
        self.__reset_types()

    def clone(self):
        return Type(*self.types())

    def add_type(self, name):
        if name not in self.__names:
            if isinstance(name, str):
                self.__names.add(name)
            else:
                self.__names |= name.types()
            self.__reset_types()

    def __reset_types(self):
        # This must be called first
        # TODO: Isolate this line to own function that is called independently
        self.__mult_type_name = "mult_type_" + "".join(self.__var_name_abbreviation(n) for n in self.types())

        self.__enum_type_mapping = {
            n: "{}_{}".format(self.type_name(), self.__var_type_abbreviation(n))
            for n in self.types()
        }

        self.__struct_attr_mapping = {n: "t{}".format(i) for i, n in enumerate(self.types())}

    def __var_name_abbreviation(self, name):
        """The struct representing the name of the type containing multiple
        types will be mult_type_ followed by the first characters of the
        contained types.

        Pointers will have the character follwed by the depth of the pointer.

        For example:
            [int] -> "int"
            [char*] -> "char*"
            [int, float] -> "mult_type_if" (or "mult_type_fi")
            [char*, char] -> "mult_type_c1c" (or "mult_type_cc1")
            [int, float, char**] -> "mult_type_ifc2" (or ...)

        TODO: Come up with better naming scheme in event of multiple vars with same first char
        """
        count = name.count("*")
        if count:
            return name[0] + str(count)
        return name[0]

    def types(self):
        return self.__names

    def num_types(self):
        return len(self.__names)

    def type_name(self):
        if len(self.__names) == 1:
            return self.__first_name
        else:
            return self.__mult_type_name

    def __str__(self):
        return self.type_name()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.type_name() == other
        elif isinstance(other, Type):
            return hash(self) == hash(other)
        else:
            raise NotImplementedError("Cannot compare Type with {}".format(type(other)))

    def __hash__(self):
        return hash(frozenset(self.__names))

    def __var_type_abbreviation(self, type_name):
        return "{}_{}".format(type_name.replace("*", ""), type_name.count("*"))

    """
    Enum types
    """

    def enum_types(self):
        return self.__enum_type_mapping.values()

    def enum_name(self):
        return "ElemType_" + self.type_name()

    def enum_typedef(self):
        return cgen.Typedef(extended_cgen.Value(
            "enum {}".format(self.enum_name()),
            self.enum_name()
        ))

    def enum_def(self):
        return extended_cgen.Enum(
            self.enum_name(),
            self.enum_types(),
            with_semicolon=True
        )

    def enum_type(self, t):
        """Return the corresponding enum type name for a given contained type."""
        return self.__enum_type_mapping[str(t)]

    """
    Multiple type struct def
    """

    def struct_attrs(self):
        return self.__struct_attr_mapping.values()

    def struct_typedef(self):
        return cgen.Typedef(extended_cgen.Value(
            "struct {}".format(self.type_name()),
            self.type_name()
        ))

    def struct_def(self):
        return extended_cgen.Struct(
            self.type_name(),
            [
                "{} type".format(self.enum_name()),
                extended_cgen.Union(
                    "",
                    ("{} {}".format(k, v) for k, v in self.__struct_attr_mapping.items())
                )
            ],
            with_semicolon=True
        )

    def attr_name(self, t):
        """Return the corresponding attribute name for the given contained type."""
        return self.__struct_attr_mapping[str(t)]


class PointerType(Type):
    def __init__(self, t):
        super().__init__(str(t) + "*")

