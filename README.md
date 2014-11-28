LITHP
=====

Lambdas ImplemenTed Handily in Python

LITHP is a LISP-like language interpreted in Python.

Grammar:

    exprList --> expr exprList | ε
    
    expr     --> NUM |
    
                 IDENTIFIER |
                 
                 (lambda IDENTIFIER . expr)
                 
                 (expr expr)