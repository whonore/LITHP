#!/usr/bin/env

WHITESPACE = (' ', '\t', '\n', '\r')
KEYWORDS = ("lambda", "def")
SYMBOLS = {
    '(': "lparen",
    ')': "rparen",
    '.': "dot",
    '=': "equal"
}
LINE = 1
COL = 1


def char_read(in_stream):
    global COL
    COL += 1
    return in_stream.read(1)


def char_peek(in_stream):
    char = in_stream.read(1)
    if char:
        pos = in_stream.tell()
        in_stream.seek(pos - 1, 0)
    return char


def next_token(in_stream):
    global COL, LINE

    char = char_read(in_stream)
    while char in WHITESPACE:
        if char in ('\n', '\r'):
            LINE += 1
            COL = 1
        char = char_read(in_stream)

    if char in SYMBOLS:
        return (SYMBOLS[char], char, (LINE, COL - 1))
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
