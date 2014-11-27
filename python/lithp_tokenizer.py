#!/usr/bin/env

WHITESPACE = (' ', '\t', '\n', '\r')


def char_read(in_stream):
    return in_stream.read(1)


def char_peek(in_stream):
    char = in_stream.read(1)
    if char:
        pos = in_stream.tell()
        in_stream.seek(pos - 1, 0)
    return char


def next_token(in_stream):  # add location for error
    char = char_read(in_stream)
    while char in WHITESPACE:
        char = char_read(in_stream)

    if char == '(':
        return ("lparen", char)
    elif char == ')':
        return ("rparen", char)
    elif char == '.':
        return ("dot", char)
    elif char.isdigit():  # change to accept decimal
        num = char
        while char_peek(in_stream).isdigit():
            num += char_read(in_stream)
        return ("num", int(num))
    elif char.isalpha():  # change to accept numbers
        ident = char
        while char_peek(in_stream).isalpha():
            ident += char_read(in_stream)
        return ("identifier", ident)
    return ("EOF", None)
