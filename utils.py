#-*- coding: utf-8 -*-

import string


def contains_chars(s, chars):
    """Checks is a string contains any character in a list of chars."""
    return any((c in chars) for c in s)


def contains_whitespace(s):
    """Check if a string contains whitespace."""
    return contains_chars(s, string.whitespace)


class SlotDefinedClass(object):
    __slots__ = tuple()

    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs[attr])

    def json(self):
        """Produce a json serializeable version of instances of this class."""
        d = {"type": type(self).__name__}
        for k in self.__slots__:
            v = getattr(self, k)
            if isinstance(v, SlotDefinedClass):
                d[k] = v.json()
            elif isinstance(v, (list, tuple)):
                d[k] = tuple(x.json() if isinstance(x, SlotDefinedClass) else x for x in v)
            else:
                d[k] = v
        return d

    def __str__(self):
        return str(self.json())
