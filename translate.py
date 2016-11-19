#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
import ast

def prettyparseprintfile(filename, spaces=4):
    with open(filename, "r") as f:
        prettyparseprint(f.read(), spaces)


def prettyparseprint(code, spaces=4):
    node = ast.parse(code)
    text = ast.dump(node)
    indent_count = 0
    i = 0
    while i < len(text):
        c = text[i]

        if text[i:i+2] in ("()", "[]"):
            i += 1
        elif c in "([":
            indent_count += 1
            indentation = spaces*indent_count
            text = text[:i+1] + "\n" + " "*indentation + text[i+1:]
        elif c in ")]":
            indent_count -= 1
            indentation = spaces*indent_count
            text = text[:i] + "\n" + " "*indentation + text[i:]
            i += 1 + indentation

            if text[i:i+3] in ("), ", "], "):
                text = text[:i+2] + "\n" + " "*indentation + text[i+3:]
                i += indentation

        i += 1
    print(text)


