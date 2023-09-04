# __version__ = "0.6.1"
from .user.problem_stack import ProbStack
from .MathFunctions.math_cmds import function


# only load magics if in ipython environment
try:
    get_ipython()
    from .magics import problem_magics
except NameError:
    pass
