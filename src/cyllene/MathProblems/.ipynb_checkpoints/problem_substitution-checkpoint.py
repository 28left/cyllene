from string import Template
import re
from sympy import latex

from cyllene2.MathProblems.problem_instantiator import instantiate_expression

IDENTIFIER_STRING = "wafuienuiwnaowfooiuaneoafwjnof"


class LatexTemplate(Template):
    # delimiter = '#'
    delimiter = "@"


def substitute_math_vars(arg_string, **kwargs):

    t = LatexTemplate(arg_string)

    return t.safe_substitute(**kwargs)


def substitute_parameter_string(arg_string, **kwargs):
    """
    Attempts to substitute all identifiers of the form @{key}
    in arg_string, using a dictionary (kwargs).
    If an identifier is unknown, try to resolve it as a math expression
    using the dictionary.
    """

    # find all substitution instances
    identifiers = re.findall("@\{.*?\}", arg_string)

    # extract keys
    new_id_string = arg_string
    key_array = []

    # replace the keys with a generic sequence a, b, c, ...
    for index, value in enumerate(identifiers):
        new_id_string = new_id_string.replace(
            value, "@{" + IDENTIFIER_STRING + str(index) + "}", 1
        )
        key_array.append(value[2:-1])

    # try to instantiate keys, save value in dict
    val_dict = {}
    string_dict = {}  # texified version of val_dict, for printing

    for index, value in enumerate(key_array):

        instance = instantiate_expression(value, kwargs)

        val_dict[IDENTIFIER_STRING + str(index)] = instance

        # unless the instantiated expression is a string, convert to latex
        if isinstance(instance, str):
            string_dict[IDENTIFIER_STRING + str(index)] = instance
        else:
            string_dict[IDENTIFIER_STRING + str(index)] = latex(instance)

    # finally try to substitute safely, using the new dict
    return substitute_math_vars(new_id_string, **string_dict)
