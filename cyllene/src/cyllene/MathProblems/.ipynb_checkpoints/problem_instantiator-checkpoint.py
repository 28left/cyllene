from sympy import sympify, Rational
from math import ceil, sqrt

from cyllene2.MathProblems.problem_aux import my_random_int, pick_from, pick_one, commas, dfraction, line_fraction

FUNCTION_DICT = {"randnum": my_random_int,
                 "pick": pick_from,
                 "pickone": pick_one,
                 "abs": abs,
                 "ceil": ceil,
                 "fraction": Rational,
                 "sqrt": sqrt,
                 "commas": commas,
                 "max": max,
                 "min": min,
                 "dfraction": dfraction,
                 "line_fraction": line_fraction
                 }


def instantiate_expression(expr, instantiation_dictionary):
    """
    Tries to instantiate an expression using 
    a dictionary of parameters (variables and functions)
    by running sympify
    """

    try:
        value = sympify(expr, locals=instantiation_dictionary | FUNCTION_DICT)

    except Exception as e:
        print("Cannot instantiate expression: ", expr)
        print(e)
        value = None

    return value
