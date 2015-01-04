LITHP
=====

Lambdas ImplemenTed Handily in Python

LITHP is a LISP-like language interpreted in Python.

Grammar:

    exprList --> expr exprList | ε
    
    expr     --> NUM |
    
                 IDENTIFIER |
                 
                 (lambda IDENTIFIER . expr) |
                 
                 (expr expr) |
                 
                 (def IDENTIFIER = expr) |
                 
                 (if expr expr expr)
                 
NUM is of the form [0-9]+(.)?[0-9]*
IDENTIFIER is of the form [a-zA-Z]+