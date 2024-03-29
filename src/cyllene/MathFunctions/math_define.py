import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
import random
from .math_randomfunction import set_function_random

FUNCTION_LIST = [
    "const",
    "linear",
    "quadratic",
    "cubic",
    "squareroot",
    "cubicroot",
    "rational",
    "exp",
    "tri",
    "log",
    "comp",
    "random",
]

# Reserve some (real-valued) symbols in Sympy
a, b, c, d, p, q, r, s, t, w, x, y, z = sp.symbols(
    'a b c d p q r s t w x y z', real=True)


def define_expression(expr, mylocals=None, eval_mode=False):
    """
    sympify an input and return a sympy expression
    together with a list of issues (optional, possibly empty)

    parameters:
        eval_mode (Boolean): should sympify try to evaluate expression
        return_issues (Boolean): should list of issues during syntax check
            be returned

    Valid arguments
    - a string
    - a constant
    - a sympy expression

    The string can be a math string or one of the following expression types:
    'const', 'linear', 'quadratic', 'cubic', 'squareroot',
    'cubicroot', 'rational', 'exp', 'tri', 'log', 'comp', 'monomial'

    One can also pass 'random' to pick an expression randomly.
    """
    # const, step, exp, trig, poly, linear, quadratic, cubic, sqrt, cbrt = sp.symbols(
    #     'const,step,exp,trig,poly,linear,quadratic,cubic,sqrt,cbrt', cls=sp.Function
    # )

    if expr in FUNCTION_LIST:

        # First check whether string argument is a keyword
        if expr == "random":
            expr = random.choice(
                [
                    "const",
                    "linear",
                    "quadratic",
                    "cubic",
                    "squareroot",
                    "cubicroot",
                    "rational",
                    "comp",
                    "exp",
                    "tri",
                    "log",
                ]
            )

        if expr == "comp":
            comp = [
                random.choice(
                    [
                        "const",
                        "linear",
                        "quadratic",
                        "cubic",
                        "squareroot",
                        "cubicroot",
                        "rational",
                        "exp",
                        "tri",
                        "log",
                    ]
                )
                for i in range(2)
            ]
            new_expr = sp.sympify(
                set_function_random("comp", comp[0], comp[1]))

        else:
            new_expr = sp.sympify(
                set_function_random(expr), locals=mylocals)

        expr_ok = True
        issues = []

    elif isinstance(expr, sp.Basic):
        # if expr is Sympy type, skip syntax check
        expr_ok = True
        new_expr = expr
        issues = []

    elif isinstance(expr, (int, float)):
        # if expr is numerical, directly sympify
        expr_ok = True
        new_expr = sp.sympify(expr, locals=mylocals, evaluate=eval_mode)
        issues = []

    elif isinstance(expr, str):

        #         try:
        #             # if input can be turned into number, do this to avoid
        #             # weird sympy bug
        #             if '1/' in expr:
        #                 # force sympy to ev
        #                 check = [Fraction(expr), True, []]
        #             elif '.' in expr:
        #                 # has decimal point, try float conversion
        #                 check = [float(expr), True, []]
        #             else:
        #                 # check integer
        #                 check = [int(expr), True, []]

        #         except ValueError:
        #             # check syntax of expr;
        #             # returns triple:
        #             #   ['sanitized' string, compilable flag (boolean), issues list]

        try:

            new_expr = parse_expr(
                expr,
                local_dict=mylocals,
                transformations=standard_transformations
                + (
                    convert_xor,
                    implicit_multiplication_application,
                ),
                evaluate=False,
            )

            # new_expr = sp.sympify(expr, locals=mylocals)
            expr_ok = True

        except:
            expr_ok = False
            issues = ["invalid syntax"]

        # check = ms.check_syntax(expr)

        # print(check)

        # if check[1]:
        #     try:
        #         new_expr = sp.sympify(
        #             check[0], locals=mylocals, evaluate=eval_mode)
        #         if new_expr.is_real:
        #             # if input is number, evaluate
        #             new_expr = sp.sympify(
        #                 check[0], locals=mylocals, evaluate=True)
        #         expr_ok = True
        #         issues = []

        #     except:
        #         expr_ok = False
        #         issues = ["invalid syntax"]

        # else:
        #     # check_syntax discovered issues
        #     expr_ok = False
        #     issues = check[2]

    else:
        # argument expr is not of the right type
        expr_ok = False
        issues = ["unknown input format"]

    if expr_ok:
        return new_expr, []
    else:
        return None, issues


def define_function(expr, mode="numerical"):
    """
    sympify an expression and return a function evaluating this expression,
    together with a list of issues (optional, possibly empty)

    This uses SymPy's lambdify function.

    parameters:
        eval_mode (Boolean): should sympify try to evaluate expression
        return_issues (Boolean): should list of issues during syntax check
            be returned
    """

    [func, issues] = define_expression(expr, eval_mode=True)

    if func:
        if mode == "numerical":
            if len(func.free_symbols) > 0:
                # if there free symbols in func, use the first as the function var
                return sp.lambdify([func.free_symbols.pop()], func)
            #     return lambda u: func.evalf(subs={x, u}, n=5)
            else:
                # otherwise any symbol will do
                return sp.lambdify([x], func)
                # return lambda u: func.evalf(subs={x, u}, n=5)

        else:
            if len(func.free_symbols) > 0:
                # if there free symbols in func, use the first as the function var
                # return sp.lambdify(func.free_symbols.pop(), func)
                return lambda u: func.subs(func.free_symbols.pop(), u)
            else:
                # otherwise any symbol will do
                # return sp.lambdify(x, func)
                return lambda u: func.subs(x, u)

    else:
        return None
