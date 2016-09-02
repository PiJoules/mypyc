#-*- coding: utf-8 -*-


class Lexer(object):
    """Lexer for splitting the text in a file into tokens."""
    def __init__(self, filename):
        self.__filename = filename

    def tokens(self):
        with open(self.__filename, "r") as f:
            for line in f:
                for c in line:
                    yield c

