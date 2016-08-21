#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from lexer import Lexer
from parser import Parser
from c_translator import CTranslator

import sys
import json


def main():
    filename = sys.argv[1]
    lexer = Lexer(filename)
    tokens = [token for token in lexer]
    assert tokens == lexer.tokens()

    print("Tokens")
    for token in tokens:
        print("'{}'".format(repr(token)))
    print("")

    parser = Parser(tokens)
    parse_tree = parser.parse()
    print("Parse tree")
    print(json.dumps(parse_tree.json(), indent=4))
    print("")

    translator = CTranslator(parse_tree)
    translation = translator.translate()
    print("C translation")
    print(translation)
    print("")

    return 0


if __name__ == "__main__":
    main()

