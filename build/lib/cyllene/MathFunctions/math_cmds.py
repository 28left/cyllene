from .math_functionclass import Function
from .math_define import FUNCTION_LIST


def function(expr):
    """
    Defines a function based on a syntax check
    and a Function object, using lambda operator.
    Returns a pure function.
    """
    func = Function(expr)

    if func.is_defined:
        return func.lambda_form
        # return lambda x: func.eval_at(x)

    else:
        issues_report = "".join(
            [
                "\t" + str(i + 1) + ". " + func.issues[i] + "\n"
                for i in range(len(func.issues))
            ]
        )
        print("Problems encountered:\n" + issues_report)
        return None
        # raise ValueError('Problems encountered:\n'+issues_report)


def random_function(arg="random"):
    """
    Pick a function at random.
    One of the folliwing types can be specified:
    'const', 'linear', 'quadratic', 'cubic', 'squareroot',
    'cubicroot', 'rational', 'exp', 'tri', 'log', 'comp',
    'random'
    """
    if arg in FUNCTION_LIST:
        func = Function(arg)
    else:
        func = Function("random")

    return func.lambda_form

    # return lambda x: func.eval_at(x)
