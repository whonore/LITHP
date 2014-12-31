#!/usr/bin/env python

import sys
import lithp_tokenizer as tokenizer
import lithp_evaluator as evaluator

next_token = tokenizer.next_token
quit = evaluator.quit


class Parser():
    def __init__(self, in_stream):
        self.in_stream = in_stream
        self.tok = next_token(self.in_stream)

    def consume(self, expect, type_or_tok=1):
        if self.tok[type_or_tok] == expect:
            self.tok = next_token(self.in_stream)
        else:
            quit("{}: Invalid token {}. Expected {}.".
                 format(self.tok[2], self.tok[type_or_tok], expect))

    def parse(self):
        type, tok, loc = self.tok

        if type == "num":
            self.consume("num", 0)
            return NumNode(tok)
        elif type == "identifier":
            self.consume("identifier", 0)
            return IDNode(tok)
        elif type == "lparen":
            self.consume("(")
            type, tok, loc = self.tok

            if tok == "lambda":
                self.consume("lambda")
                type, tok, loc = self.tok

                self.consume("identifier", 0)
                id = IDNode(tok)

                self.consume(".")

                expr = self.parse()

                self.consume(")")

                return LambdaNode(id, expr)

            elif tok == "def":
                self.consume("def")
                type, tok, loc = self.tok

                self.consume("identifier", 0)
                id = IDNode(tok)

                self.consume("=")

                expr = self.parse()

                self.consume(")")

                return DefineNode(id, expr)

            lexpr = self.parse()
            rexpr = self.parse()

            self.consume(")")

            return AppNode(lexpr, rexpr)
        elif type == "EOF":
            self.consume("EOF", 0)
            return None
        else:
            quit("{}: Did not expect {} at this time.".format(loc, tok))


class NumNode():
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "NumNode({})".format(str(self.val))

    def __str__(self):
        return str(self.val)


class IDNode():
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "IDNode({})".format(str(self.val))

    def __str__(self):
        return str(self.val)


class LambdaNode():
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __repr__(self):
        return ("LambdaNode(\nID: {}\nExpr: {})".
                format(str(self.id), str(self.expr)))

    def __str__(self):
        return "(lambda {} . {})".format(str(self.id), str(self.expr))


class DefineNode():
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def __repr__(self):
        return ("DefineNode(\nID: {}\nExpr: {})".
                format(str(self.id), str(self.expr)))

    def __str__(self):
        return "(def {} = {})".format(str(self.id), str(self.expr))


class AppNode():
    def __init__(self, lexpr, rexpr):
        self.lexpr = lexpr
        self.rexpr = rexpr

    def __repr__(self):
        return ("AppNode(\nLexpr: {}\nRexpr: {})".
                format(str(self.lexpr), str(self.rexpr)))

    def __str__(self):
        return "({} {})".format(str(self.lexpr), str(self.rexpr))
