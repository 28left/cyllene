import random as rd
import sympy as sp


def my_random_int(a: int, b: int, *args):
    """
    return a random number between a and b (inclusive)
    - with stepwidth step
    - exclude numbers in exclude
    """

    rd.seed()

    step = 1
    exclude = set()

    if len(args) == 1:
        if isinstance(args[0], set) or isinstance(args[0], tuple) or isinstance(args[0], list):
            # only argument is an exclude list/tuple/set
            exclude = set(args[0])
        else:
            step = args[0]

    if len(args) == 2:
        step = args[0]
        if isinstance(args[1], set) or isinstance(args[1], tuple) or isinstance(args[1], list):
            # exclude is given as list/tuple/set
            exclude = set(args[1])
        else:
            # exclude is given as single number -> add to set
            exclude.add(args[1])

    try:
        # print(
        #     f"generating random int between {a} and {b}, stepwidth {step}, exclude {exclude}"
        # )

        while True:

            r = rd.randrange(a, b + 1, step)

            if r not in exclude:
                break

        return r

    except TypeError or ValueError:

        print("random: range and step inputs must be integers, exclude must be a set")
        return None


def pick_from(number, *args, exception=None):

    while True:
        rd_array = rd.sample(args, number)

        if exception != None:
            if not exception in rd_array:
                break
        else:
            break

    return rd_array


def pick_one(*args):

    return rd.sample(args, 1)[0]


def commas(value):
    try:
        if (isinstance(value, type(sp.Integer(2)))):
            value = int((value).evalf())
        elif (isinstance(value, type(sp.Float(2.12)))):
            value = (value).evalf()
            value = "{:.2f}".format(value)
        formatted = "{:,}".format(value)
        return formatted
    except:
        return value


def dfraction(*args):
    """
    If arg is a single value, test whether it is a fraction and if so, return it as display frac string (latex).

    If arg is a pair, interpret it as numerator and denominator and return this fraction as dfrac string.
    """
    if len(args) == 1:
        frac = sp.fraction(args[0])

        if frac[1] == 1:
            return frac[0]
        else:
            return '\dfrac{' + str(frac[0]) + '}{' + str(frac[1]) + '}'

    elif len(args) == 2:

        n = args[0]/sp.gcd(args[0], args[1])
        d = args[1]/sp.gcd(args[0], args[1])

        if d == 1:
            return str(n)
        else:
            return sign_symbol_neg(n*d) + '\dfrac{' + str(sp.Abs(n)) + '}{' + str(sp.Abs(d)) + '}'

    else:
        return None


def line_fraction(*args):
    """
    If arg is a single value, test whether it is a fraction and if so, return it as line frac string "a/b".

    If arg is a pair, interpret it as numerator and denominator and return this fraction as line fraction string.
    """
    if len(args) == 1:
        frac = sp.fraction(args[0])

        if frac[1] == 1:
            return frac[0]
        else:
            return str(frac[0]) + '/' + str(frac[1])

    elif len(args) == 2:

        n = args[0]/sp.gcd(args[0], args[1])
        d = args[1]/sp.gcd(args[0], args[1])
        if d == 1:
            return str(n)
        else:
            return str(n) + '/' + str(d)

    else:
        return None


def if_else(test_value: float, compared_to: float, comparison_type: str, command_true: str, command_false: str, *args):
    """
    return command_true if condition is satisfied, and command_false otherwise
    - if comparison_type == "=", condition is whether test_value == compared_to?
    - if comparison_type == ">", condition is whether test_value > compared_to?
    - etc. for "<", ">=", "<=".
    - Haven't incorporated anything involving "!"
    """
    if (comparison_type == "="):
        # print("== case: testing whether", test_value, "==",
        #       compared_to, ":", test_value == compared_to)
        return command_true if test_value == compared_to else command_false
    if (comparison_type == ">"):
        # print("> case: testing whether", test_value, ">",
        #       compared_to, ":", test_value > compared_to)
        return command_true if test_value > compared_to else command_false
    if (comparison_type == ">="):
        # print(">= case: testing whether", test_value, ">=",
        #       compared_to, ":", test_value >= compared_to)
        return command_true if test_value >= compared_to else command_false
    if (comparison_type == "<"):
        # print("< case: testing whether", test_value, "<",
        #       compared_to, ":", test_value < compared_to)
        return command_true if test_value < compared_to else command_false
    if (comparison_type == "<="):
        # print("<= case: testing whether", test_value, "<=",
        #       compared_to, ":", test_value <= compared_to)
        return command_true if test_value <= compared_to else command_false
    else:
        return command_true


def sign_symbol(value: float):
    return "-" if value < 0 else "+"


def sign_symbol_neg(value: float):
    return "-" if value < 0 else ""
