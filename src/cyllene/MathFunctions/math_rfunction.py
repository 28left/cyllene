import sympy as sp
from sympy.calculus.util import continuous_domain

from .math_define import define_expression


class RFunction:

    """
    Basic class to represent a single-variable, real-valued
    function. 

    Attributes:
    -----------
    sym_form : sympy Basic
        sympy expression giving a symbolic representation of the function
    variable : sympy Symbol
        variable symbol of the function expression(default: x)
    lambda : function
        lambda form of function for easy evaluation
    domain : sympy Set
        domain of the function (can be subset of largest possible domain given by sym_form)
    table : list
        table of function values [[x_1, y_1], ..., [x_n,y_n]]
    valid : bool
        flag whether function is properly defined or just dummy placeholder
    """

    def __init__(self, data, variable="x", mylocals=None):
        """Initialize the RFunction object. 

        Parameters
        ----------
        data : str, sympy Basic, or list
            data used to initialized the function
        variable : str
            name of variable used by Sympy
        mylocals : dict
            dictionary to be used by sympy parser

        As data, one can pass one of
            - string: will be sent to sympy parser to try and turn it into sympy expression
            - sympy expression
            - list: should be of format [[x_1, y_1], ..., [x_n,y_n]]
        If initialization fails, attributes are filled with dummy assignments
        """

        # Initialize all basic function attributes with dummy values
        self.sym_form = sp.sympify('0')
        self.table = {}
        self.variable = sp.Symbol('x', real=True)
        self.lambda_form = sp.lambdify(
            self.variable, self.sym_form, modules="sympy")
        self.domain = sp.EmptySet
        self.status = "undefined"

        if isinstance(data, list):
            # function is given as table
            # initialize from subroutine
            self.set_function_from_table(data, variable)

        else:
            # send to subroutine to parse string or set sympy expression directly
            self.set_function_from_expression(data, variable, mylocals)

    def set_function_from_expression(self, data, variable='x', mylocals=None):
        """Instantiate a function from an expression

        Parameters
        ----------
        data : str or sympy Basic
            expression representing the function
        variable : str
            variable to be used in symbolic representation
        mylocals : dict
            dictionary to be used by sympy parser
        """

        try:
            self.variable = sp.Symbol(variable, real=True)
        except ValueError:
            raise ValueError(str(variable) + " is not a valid variable")

        [new_expr, self.issues] = define_expression(
            data, mylocals, eval_mode=True
        )

        if new_expr:
            # input ok
            self.status = "symbolic"

            # Initialize all basic function attributes
            self.sym_form = new_expr
            self.lambda_form = sp.lambdify(
                self.variable, self.sym_form, modules="sympy")
            self.domain = continuous_domain(
                self.sym_form, self.variable, sp.S.Reals)

    def set_function_from_table(self, data: list, variable="x"):
        """Instantiate a function from a list of values

        Parameters
        ----------
        data : list
            finite list of [x,y] pairs
        variable : str
            variable to be used in symbolic representation
        """

        if not isinstance(data, list):
            raise TypeError("Input must be a list of [x,y] pairs")

        try:
            self.variable = sp.Symbol(variable, real=True)
        except ValueError:
            raise ValueError(str(variable) + " is not a valid variable")

        # Assemble a function (with finite domain) with the given values,
        # using sympy Piecewise

        try:
            condition_list = []
            for _ in data:
                condition_list.append((sp.nan, self.variable < _[0]))
                condition_list.append((_[1], self.variable <= _[0]))

            self.sym_form = sp.piecewise_exclusive(
                sp.Piecewise(*condition_list))
            self.domain = sp.Union(*[{_[0]} for _ in data])
            self.table = data
            self.lambda_form = sp.lambdify(
                self.variable, self.sym_form, modules="sympy")
            self.status = "finite"
        except ValueError:
            raise ValueError("Invalid value list")
