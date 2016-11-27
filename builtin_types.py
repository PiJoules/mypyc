# -*- coding: utf-8 -*-


class Type(object):
    def __init__(self, name):
        self.__first_name = name
        self.__names = set([name])
        self.__reset_mult_type_name()

    def add_type(self, name):
        if name not in self.__names:
            if isinstance(name, str):
                self.__names.add(name)
            else:
                self.__names |= name.types()
            self.__reset_mult_type_name()

    def __reset_mult_type_name(self):
        self.__mult_type_name = "mult_type_" + "".join(self.__var_name_abbreviation(n) for n in self.__names)

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
            #return self.type_name() == other.type_name()
            return hash(self) == hash(other)
        else:
            raise NotImplementedError("Cannot compare Type with {}".format(type(other)))

    def __hash__(self):
        return hash(frozenset(self.__names))


class PointerType(Type):
    def __init__(self, t):
        super().__init__(str(t) + "*")

