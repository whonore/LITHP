#!/usr/bin/env python

WHITESPACE = (' ', '\t', '\n', '\r')
KEYWORDS = ("lambda", "def", "if")
RESERVED_VALUES = {
    ":t": 1,
    ":f": 0
}
SYMBOLS = {
    '(': "lparen",
    ')': "rparen",
    '.': "dot",
    '=': "equal"
}
LINE = 1
COL = 1


def char_read(in_stream):
    global COL, LINE
    char = in_stream.read(1)

    COL += 1
    if char in ('\n', '\r'):
        LINE += 1
        COL = 1

    return char


def char_peek(in_stream):
    char = in_stream.read(1)
    if char:
        pos = in_stream.tell()
        in_stream.seek(pos - 1, 0)
    return char


def next_token(in_stream):
    char = char_read(in_stream)

    if char in WHITESPACE:
        return next_token(in_stream)

    if char == "%":            # Eat comment
        while char not in ('\n', '\r', ''):
            char = char_read(in_stream)
        return next_token(in_stream)

    if char in SYMBOLS:
        return (SYMBOLS[char], char, (LINE, COL - 1))

    elif char == ':':
        val = char
        while char_peek(in_stream).isalpha():
            char = char_read(in_stream)
            val += char
        return ("num", RESERVED_VALUES[val], (LINE, COL - len(val)))

    elif char.isdigit():
        num = char
        while char_peek(in_stream).isdigit():
            num += char_read(in_stream)
        if char_peek(in_stream) == ".":
            num += char_read(in_stream)
            while char_peek(in_stream).isdigit():
                num += char_read(in_stream)
        return ("num", float(num), (LINE, COL - len(num)))

    elif char.isalpha():
        ident = char
        while char_peek(in_stream).isalpha():
            ident += char_read(in_stream)

        if ident in KEYWORDS:
            return ("keyword", ident, (LINE, COL - len(ident)))
        return ("identifier", ident, (LINE, COL - len(ident)))
    return ("EOF", None, (LINE, COL))
