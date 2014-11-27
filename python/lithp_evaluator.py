#!/usr/bin/env

import sys
import lithp_parser as parser

isa = isinstance


def quit(msg):
    sys.exit(msg)


def main(input):
    with open(input) as file:
        p = parser.Parser(file)
        tree = p.parse()
        expr = evaluate(tree, {})

        if isa(expr, tuple):
            print("<lambda {} . {}, {}>".
                  format(expr[0][0], expr[0][1], expr[1]))
        else:
            print(expr)


def evaluate(tree, env):
    if isa(tree, parser.NumNode):
        return tree.val
    elif isa(tree, parser.IDNode):
        try:
            return env[tree.val]
        except KeyError:
            quit("Undefined identifier: {}.".format(tree.val))
    elif isa(tree, parser.LambdaNode):
        return ((tree.id.val, tree.expr), env)
    elif isa(tree, parser.AppNode):
        try:
            right = evaluate(tree.rexpr, env)
            left = evaluate(tree.lexpr, env)
            left[1][left[0][0]] = right
            return evaluate(left[0][1], left[1])
        except RuntimeError:
            quit("Recursion depth exceeded. ({})".
                 format(str(sys.getrecursionlimit())))
    else:
        quit("Error.")

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        quit("Please provide a file to evaluate.")
