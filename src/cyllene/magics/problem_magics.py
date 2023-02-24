from ..user.problem_cmds import make_problem, make_qti, show_problem
# from ..user.problem_stack import ProbStack

from .. import ProbStack
from IPython.core.magic import register_cell_magic, register_line_magic


@register_cell_magic
def makeproblem(line, cell):

    webassign = False

    params = line.split()
    if "-wa" in params:
        webassign = True
        params.remove("-wa")

    if len(params) > 0:
        pname = params[0]
    else:
        pname = ""

    ProbStack.update_user_funcs()
    p = make_problem(cell, ProbStack.user_funcs, webassign)
    ProbStack.add(p, pname)


@register_line_magic
def makeqti(line):

    if "-nosol" in line:
        with_solution = False
        line = line.replace("-nosol", "")
    else:
        with_solution = True

    params = line.rpartition(',')
    if params[1] == '':
        pname = params[2]
        pnum = 1
    else:
        pname = params[0]
        try:
            pnum = int(params[2])
        except ValueError:
            pnum = 1

    ProbStack.update_user_funcs()
    p = ProbStack.get(pname)

    make_qti(p, pnum, solution=with_solution, externals=ProbStack.user_funcs)


@register_line_magic
def showproblem(line):

    p = ProbStack.get(line)
    if p:
        show_problem(p)
    else:
        print("Problem not found")
