from sympy import sympify, Rational
from math import ceil, sqrt

from .problem_aux import my_random_int as randnum
from .problem_aux import pick_one as pickone
from .problem_aux import pick_from as pick
from .problem_aux import dfraction as dfraction
from .problem_aux import line_fraction as line_fraction
from .problem_aux import commas as commas
from ..MathFunctions.math_cmds import function

FUNCTION_DICT = {"randnum": randnum,
                 "pick": pick,
                 "pickone": pickone,
                 "abs": abs,
                 "ceil": ceil,
                 "fraction": Rational,
                 "sqrt": sqrt,
                 "commas": commas,
                 "max": max,
                 "min": min,
                 "dfraction": dfraction,
                 "line_fraction": line_fraction,
                 "function": function
                 }


def instantiate_expression(expr, instantiation_dictionary):
    """
    Tries to instantiate an expression using 
    a dictionary of parameters (variables and functions)
    by running sympify
    """

    try:
        value = sympify(expr, locals=instantiation_dictionary |
                        FUNCTION_DICT | __builtins__)

    except Exception as e:
        print("Cannot instantiate expression: ", expr)
        print(e)
        value = None

    return value


# def instantiate_string_parameters(value, val_dict):

#     if isinstance(value, str):
#         value = substitute_parameter_string(value, **val_dict)
#     elif isinstance(value, list):
#         for index, v in enumerate(value):
#             value[index] = instantiate_string_parameters(v, val_dict)

#     return value


def code_to_parameter(code_string: str, externals={}):

    # print(code_string)
    exec(code_string)

    # print(locals())
    param_dict = locals()
    param_dict.pop('code_string')

    # print(param_dict)
    # for key in param_dict:
    #     param_dict[key] = instantiate_string_parameters(
    #         param_dict[key], param_dict)

    return param_dict
