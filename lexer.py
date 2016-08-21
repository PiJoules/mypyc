#-*- coding: utf-8 -*-

from tokens import *


class NoMoreLinesException(Exception):
    """No more lines are available in the file."""
    pass


class Lexer(object):
    """Lexer for splitting the text in a file into tokens."""
    def __init__(self, filename):
        self.__filename = filename
        self.__file = open(filename, "r")
        self.__buffer = []
        self.__tokens = []

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

    def __token_strings_to_objs(self, tokens):
        """Convert a list of token strings to token objects."""
        token_objs = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isalpha():
                token_objs.append(Word(chars=token))
            elif token.isdigit():
                # Try to form decimals or whoe numbers
                # TODO: Support other numeric types in other bases
                if tokens[i+1] == ".":
                    assert tokens[i+2].isdigit()
                    token_objs.append(DecimalNumber(value=float(
                        str(token) + "." + str(tokens[i+2])
                    )))
                    i += 2
                else:
                    token_objs.append(WholeNumber(value=int(token)))
            elif token == "\n":
                token_objs.append(Newline())
            elif token == " ":
                # TODO: Account for tabs
                # Combine words separated by spaces in literal strings
                if not token_objs or isinstance(token_objs[-1], Newline):
                    # Indentation is space at start of line
                    size = 0
                    while i < len(tokens) and tokens[i] == " ":
                        size += 1
                        i += 1
                    token_objs.append(Indentation(size=size))
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
                token_objs.append(StringToken(chars=str_literal))
            else:
                token_objs.append(Symbol(char=token))
            i += 1
        return token_objs

    def __tokenize_line(self, line):
        """Split a line into tokens."""
        tokens = [""]
        last_idx = 0

        # Read characters at a time and form strings to be tokenized
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
        return self.__token_strings_to_objs(tokens)

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
        # If have explored the whole file, return an iterator for the internal
        # token buffer.
        if self.has_next():
            while self.has_next():
                token = self.next()
                self.__tokens.append(token)
                yield token
        else:
            for x in self.__tokens:
                yield x

    def tokens(self):
        """Return a complete list of all the tokens from the file."""
        # Be sure to flush out the rest of the file if not fully explored
        while self.has_next():
            token = self.next()
            self.__tokens.append(token)
        return self.__tokens

