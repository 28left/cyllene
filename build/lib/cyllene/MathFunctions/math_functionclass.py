import sympy as sp

from .math_listform import string_to_list
from .math_define import define_expression


class Function:

    """
    Basic class to represent a single-variable, real-valued
    function. Every function has four basic attributes:
    - sympy expression
    - tree form
    - table
    - graph
    """

    def __init__(self, expr, variable="x", mylocals=None):

        self.variable = sp.Symbol(variable, real=True)
        self.locals = mylocals

        # try:

        #     parse_expr(expr,
        #         transformations=standard_transformations+(convert_xor,implicit_multiplication_application,),
        #         evaluate=False)

        #     new_expr = sp.sympify(expr, locals=self.locals)
        #     self.is_defined = True

        # except:
        #     new_expr = sp.sympify(0)

        [new_expr, self.issues] = define_expression(
            expr, mylocals=self.locals, eval_mode=True
        )

        if new_expr:
            # input ok
            self.is_defined = True
        else:
            # Initialize zero function and set flag
            self.is_defined = False
            new_expr = sp.sympify(0)

        # Initialize all basic function attributes
        self.sym_form = new_expr
        self.str_form = str(new_expr).replace("**", "^")
        self.list_form = string_to_list(self.str_form)
        self.tex_form = sp.latex(self.sym_form)
        self.table_form = {}
        # self.graph_form = plt.figure()

        # initialize further attributes of a function
        # variables = fa.get_variables(self.sym_form)
        # string_variables = [str(var) for var in variables]
        # string_variables.sort()
        # self.variables = [MYLOCALS_LAMBDA[var_string] for var_string in string_variables] # do this to sort variables alphabetically

        # self.variables = fa.get_variables(self.sym_form)
        self.lambda_form = sp.lambdify(
            self.variable, self.sym_form, modules="sympy")

        # parameters for piecewise functions (currently not activated)
        # self.breakpoints = {}
        # self.functions = {}
        # self.right_endpoints = {}

        # get the domain
        """
        get_domain method from sympy does not seem stable currently
        (as of Nov 15, 2020) -- disabled for now
        """
        # self.domain = fa.get_domain(self.sym_form)

    def __add__(a, b):
        c = Function(a.sym_form + b.sym_form)
        return c
