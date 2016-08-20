#!/usr/bin/env python


def contains_chars(s, chars):
    """Checks is a string contains any character in a list of chars."""
    return any((c in chars) for c in s)


def contains_whitespace(s):
    import string
    return contains_chars(s, string.whitespace)


class Token(object):
    def __ne__(self, other):
        return not (self == other)


class StringToken(Token):
    """Series of characters."""
    def __init__(self, chars):
        self.__chars = chars

    def __repr__(self):
        return "<{} ({})>".format(type(self).__name__, self.__chars)

    def chars(self):
        return self.__chars

    @classmethod
    def check_word(cls, word, chars=None):
        assert isinstance(word, cls)
        if chars:
            assert chars == word.chars()

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.__chars
        if not isinstance(other, type(self)):
            return False
        return other.chars() == self.__chars

    def __str__(self):
        return self.__chars


class Word(StringToken):
    """Series of non-whitespace characters."""
    def __init__(self, chars):
        assert not contains_whitespace(chars)
        super(Word, self).__init__(chars)


class Indentation(Token):
    def __init__(self, size):
        self.__size = size

    def __repr__(self):
        return "<Indentation (size={})>".format(self.__size)

    def size(self):
        return self.__size

    def __eq__(self, other):
        if not isinstance(other, Indentation):
            return False
        return self.__size == other.size()

    @classmethod
    def check_indentation(cls, ind, size=None):
        assert isinstance(ind, Indentation)
        if size is not None:
            assert ind.size() == size

    def __str__(self):
        return " " * self.__size


class Newline(Token):
    def __repr__(self):
        return "<Newline>"

    def __eq__(self, other):
        return isinstance(other, Newline)

    @classmethod
    def check_newline(cls, symbol):
        assert isinstance(symbol, Newline)

    def __str__(self):
        return "\n"


class Symbol(Token):
    def __init__(self, char):
        self.__char = char

    def __repr__(self):
        return "<Symbol ('{}')>".format(self.__char)

    def char(self):
        return self.__char

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.__char
        if not isinstance(other, Symbol):
            return False
        return self.__char == other.char()

    @classmethod
    def check_symbol(cls, symbol, char=None):
        assert isinstance(symbol, Symbol)
        if char:
            assert symbol.char() == char

    def __str__(self):
        return self.__char


class NoMoreLinesException(Exception):
    """No more lines are available in the file."""
    pass


class Lexer(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__file = open(filename, "r")
        self.__buffer = []

    def has_next(self):
        """
        Check if there are any more tokens that can be popped.
        Automatically adds tokens if buffer is empty.
        """
        if self.__buffer:
            return True

        try:
            self.__add_tokens()
        except NoMoreLinesException:
            return False
        return True

    def __tokenize_line(self, line):
        """Split a line into tokens"""
        tokens = [""]
        last_idx = 0

        for c in line:
            if c.isalnum():
                # Add new char to last buffer
                tokens[last_idx] += c
            else:
                # Whitespace or other
                if not tokens[last_idx]:
                    tokens[last_idx] = c
                else:
                    tokens.append(c)
                    last_idx += 1
                tokens.append("")
                last_idx += 1

        # Remove last empty string
        if not tokens[last_idx]:
            tokens = tokens[:-1]

        # Convert words to token objects
        token_objs = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isalnum():
                token_objs.append(Word(token))
            elif token == "\n":
                token_objs.append(Newline())
            elif token == " ":
                if not token_objs or isinstance(token_objs[-1], Newline):
                    # Indentation is space at start of line
                    size = 0
                    while i < len(tokens) and tokens[i] == " ":
                        size += 1
                        i += 1
                    token_objs.append(Indentation(size))
                    continue
            elif token == "\"":
                # Construct string literal
                str_literal = token
                i += 1
                while True:
                    token = tokens[i]
                    if token == "\"":
                        # End of string literal
                        str_literal += token
                        break
                    elif token == "\\":
                        # Escaped next character
                        str_literal += token + tokens[i + 1]
                        i += 2
                    else:
                        # Regular word
                        str_literal += token
                        i += 1
                token_objs.append(StringToken(str_literal))
            else:
                token_objs.append(Symbol(token))
            i += 1

        return token_objs

    def __add_tokens(self):
        """Add tokens from the file to the buffer."""
        try:
            line = next(self.__file)
        except StopIteration:
            raise NoMoreLinesException()

        # Split the line by whitespace
        tokens = self.__tokenize_line(line)
        if tokens:
            self.__buffer += tokens
        else:
            raise NoMoreLinesException()

    def next(self):
        """Pop a token from the buffer."""
        return self.__buffer.pop(0)

    def __iter__(self):
        while self.has_next():
            yield self.next()

    def tokens(self):
        return self.__tokens

