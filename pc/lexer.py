# -*- coding: utf-8 -*-

from symbols import *
from tokens import *


class Lexer(object):
    def __init__(self, filename, indent_count=4):
        self.__filename = filename
        self.__generator = self.__char_generator()
        self.__tok_gen = self.__token_generator()
        self.__indent_count = indent_count

    def __char_generator(self):
        with open(self.__filename, "r") as f:
            self.__line_no = 1
            for line in f:
                self.__col_no = 1
                for c in line:
                    yield c
                    self.__col_no += 1
                self.__line_no += 1

    def __next_char(self):
        return next(self.__generator, "")

    def __token_generator(self):
        c = self.__next_char()

        word = ""
        word_line_no = self.__line_no
        word_col_no = self.__col_no

        space_count = 0  # Count num of spaces
        space_line_no = self.__line_no
        space_col_no = self.__col_no

        while c:
            if c == SPACE:
                if word:
                    yield Word(
                        line_no=word_line_no,
                        col_no=word_col_no,
                        value=word
                    )
                    word = ""

                # Record and indent
                if not space_count:
                    space_line_no = self.__line_no
                    space_col_no = self.__col_no
                space_count += 1
                if space_count >= self.__indent_count:
                    yield Indent.from_size(self.__line_no, self.__col_no, space_count)
                    space_count = 0
            else:
                # Reset space counter
                space_count = 0
                if c.isdigit():
                    num = ""
                    num_line_no = self.__line_no
                    num_col_no = self.__col_no
                    while c.isdigit():
                        num += c
                        c = self.__next_char()
                    yield Number(
                        line_no=num_line_no,
                        col_no=num_col_no,
                        value=num
                    )

                    # Already read the next character
                    continue
                elif c.isalnum() or c == UNDERSCORE:
                    if not word:
                        word_line_no = self.__line_no
                        word_col_no = self.__col_no
                    word += c
                elif c == D_QUOTE:
                    c = self.__next_char()
                    quote = ""
                    quote_line_no = self.__line_no
                    quote_col_no = self.__col_no
                    while c != D_QUOTE:
                        quote += c
                        c = self.__next_char()
                    yield Quote(
                        line_no=quote_line_no,
                        col_no=quote_col_no,
                        value="\"{}\"".format(quote)
                    )
                else:
                    # Space, newline, or symbol
                    # Pop word
                    if word:
                        yield Word(
                            line_no=word_line_no,
                            col_no=word_col_no,
                            value=word
                        )
                        word = ""

                    if c == NEWLINE:
                        yield Newline.from_location(self.__line_no, self.__col_no)

                        # Skip any following newlines
                        c = self.__next_char()
                        while c == NEWLINE:
                            c = self.__next_char()
                        continue
                    else:
                        yield Symbol(
                            line_no=self.__line_no,
                            col_no=self.__col_no,
                            value=c
                        )
            c = self.__next_char()

    def next_token(self):
        return next(self.__tok_gen, None)

