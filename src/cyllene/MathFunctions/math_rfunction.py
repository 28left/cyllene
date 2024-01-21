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
        self.variable = sp.Symbol(variable, real=True)
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

        [new_expr, _] = define_expression(
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

    @property
    def zeros(self):
        if self.status == 'symbolic':
            return sp.solveset(self.sym_form, self.variable, domain=sp.S.Reals)
        elif self.status == 'finite':
            zeros = sp.EmptySet
            for a in self.domain:
                if a == 0:
                    zeros.union({a})
            return zeros
        else:
            return None

    @property
    def critical_points(self):

        if self.status == 'symbolic':
            # for symbolic functions, follow usual def of critical point
            diff = sp.diff(self.sym_form, self.variable)
            non_def = sp.Complement(self.domain, continuous_domain(
                diff, self.variable, sp.S.Reals))
            diff_zeros = sp.solveset(diff, self.variable, domain=sp.S.Reals)

            return sp.Union(non_def, diff_zeros)
        elif self.status == 'finite':
            # for finite functions, every point is a critical point
            return self.domain
        else:
            return None

    @property
    def inflection_points(self):

        if self.status == 'symbolic':
            # for symbolic function, find args for potential inflection points
            # following the usual procedure
            diff_two = sp.diff(
                sp.diff(self.sym_form, self.variable), self.variable)
            non_def = sp.Complement(self.domain, continuous_domain(
                diff_two, self.variable, sp.S.Reals))
            diff_zeros = sp.solveset(
                diff_two, self.variable, domain=sp.S.Reals)

            return sp.Union(non_def, diff_zeros)
