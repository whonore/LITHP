#!/usr/bin/env python

import sys
import lithp_parser as parser

isa = isinstance
GLOBAL_ENV = {}


def quit(msg):
    sys.exit(msg)


def evalFile(input):
    with open(input) as file:
        p = parser.Parser(file)
        tree = p.parse()

        type, expr = evaluate(tree, {})
        while True:
            printResult(type, expr)
            tree = p.parse()
            if tree is None:
                break
            type, expr = evaluate(tree, {})


def printResult(type, expr):
    if type == "closure":
        print("<lambda {} . {}, {}>".
              format(expr[0][0], expr[0][1], expr[1]))  # for debugging only
        # print("<function>")
    elif type == "value":
        print(expr)


def evaluate(tree, env):
    if isa(tree, parser.NumNode):
        return ("value", tree.val)
    elif isa(tree, parser.IDNode):
        if tree.val in env:
            return env[tree.val]
        elif tree.val in GLOBAL_ENV:
            return GLOBAL_ENV[tree.val]
        quit("Undefined identifier: {}.".format(tree.val))
    elif isa(tree, parser.LambdaNode):
        return ("closure", ((tree.id.val, tree.expr), env))
    elif isa(tree, parser.DefineNode):
        GLOBAL_ENV[tree.id.val] = evaluate(tree.expr, env)
        return ("definition", None)
    elif isa(tree, parser.AppNode):
        try:
            rtype, right = evaluate(tree.rexpr, env)
            ltype, left = evaluate(tree.lexpr, env)

            if ltype != "closure":
                quit("Cannot apply to non-function.")

            rest, new_env = left
            id, new_expr = rest
            new_env[id] = (rtype, right)

            return evaluate(new_expr, new_env)
        except RuntimeError:
            quit("Recursion depth exceeded. ({})".
                 format(str(sys.getrecursionlimit())))
    else:
        quit("Error.")

if __name__ == "__main__":
    try:
        evalFile(sys.argv[1])
    except IndexError:
        quit("Please input file.")
    except IOError:
        quit("Given file could not be opened or does not exist.")
