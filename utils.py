#-*- coding: utf-8 -*-

import string


def contains_chars(s, chars):
    """Checks is a string contains any character in a list of chars."""
    return any((c in chars) for c in s)


def contains_whitespace(s):
    """Check if a string contains whitespace."""
    return contains_chars(s, string.whitespace)


class SlotDefinedClass(object):
    # Type names.
    # Only checks upper most type (i.e. can determine type of variable
    # to be a list, but cannot make assertions regarding the types of the
    # list contents.
    __slots__ = ()

    # Expected type for each slot
    __types__ = ()

    TYPE_MEMBER = "__cls__"

    def __init__(self, **kwargs):
        types = self.__types__
        for i, attr in enumerate(self.__slots__):
            v = kwargs[attr]
            if i < len(types):
                assert isinstance(v, types[i]), "Expected {} to be of type '{}'. Found type '{}'".format(v, types[i].__name__, type(v).__name__)
            setattr(self, attr, v)

    def dict(self):
        """Return a shallow dictionary representation of this instance for easy kwargs unpacking."""
        return {k: getattr(self, k) for k in self.__slots__}

    def json(self):
        """Produce a json serializeable version of instances of this class."""
        assert getattr(self, self.TYPE_MEMBER, None) is None
        d = {self.TYPE_MEMBER: type(self).__name__}
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

    def __eq__(self, other):
        """Just check the type and each of the attributes."""
        if not isinstance(self, type(other)):
            return False
        return all(getattr(self, attr) == getattr(other, attr) for attr in self.__slots__)

    def __ne__(self, other):
        return not (self == other)
