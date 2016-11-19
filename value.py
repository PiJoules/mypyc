# -*- coding: utf-8 -*-

import ast


class Value(object):
    def __init__(self, node):
        pass

    def type(self):
        raise NotImplementedError


def value_from_node(node):
    if isinstance(node, ast.BinOp):
        # TODO: Smarter implementation of evaluating the range of values
        return "int"
    else:
        raise RuntimeError("Unknown value node {}".format(node))
