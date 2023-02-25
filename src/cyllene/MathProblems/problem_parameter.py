from hashlib import new
from .problem_basic import Problem, ExpressionProblem
from .problem_instantiator import instantiate_expression, code_to_parameter
from .problem_substitution import substitute_parameter_string


class ParameterProblem(Problem):

    def __init__(self, my_dict={}, externals={}):

        self.set_core_attributes()

        self.keys = ["statement", "answer",
                     "problem_id", "solution",
                     "tags", "title", "parameters"]

        if isinstance(my_dict, dict) and my_dict != {}:
            self.load_dict(my_dict)

        if isinstance(externals, dict) and externals != {}:
            self.user_vars = externals

    def set_core_attributes(self):

        super().set_core_attributes()

        self.parameters = {}
        self.user_vars = {}
        self.value_dict = {}
        self.instantiated_dict = {}

    def instantiate_problem(self, externals={}):
        """
        Instantiate problem statement and solution. The user can supply its own dictionary with functions and variables. The internal problem dictionary (value_dict) is used, too.

        Keyword arguments:
        external_parameters -- dictionary to be used for parameter evaluation (default {})
        """

        # Determine which user supplied parameters should be used
        if externals:
            external_parameters = externals
        else:
            external_parameters = self.user_vars

        # Initialize the problem parameter dictionary
        self.value_dict = {}

        # First check whether parameters are given as python code
        if "code" in self.parameters:
            # in this case execute the code and use the results as value dict
            self.value_dict = code_to_parameter(
                self.parameters["code"], external_parameters)

        else:

            # instantiate parameters one by one
            for key in self.parameters:

                value = instantiate_expression(
                    self.parameters[key], dict(external_parameters, **self.value_dict))

                # if instantiation went ok, add value to dictionary
                if value == None:
                    print("Could not instantiate ", self.parameters[key])
                else:
                    self.value_dict[key] = value

        self.instantiated_dict["statement"] = substitute_parameter_string(
            self.statement, **(dict(external_parameters, **self.value_dict))
        )

        self.instantiated_dict["answer"] = substitute_parameter_string(
            self.answer, **(dict(external_parameters, **self.value_dict))
        )

        self.instantiated_dict["solution"] = substitute_parameter_string(
            self.solution, **(dict(external_parameters, **self.value_dict))
        )

    def get_problem(self, externals={}):
        """
        return a single instantiated problem as Problem

        Returns: Problem

        Keyword arguments:
        externals -- dictionary to be used for parameter evaluation (default {})
        """
        self.instantiate_problem(externals)
        return Problem(dict(self.instantiated_dict, **{"title": self.title,
                                                       "tags": self.tags,
                                                       "problem_id": self.problem_id}))

    def get_list_dict(self, num_problems: int, externals={}, duplicate_ok=False):
        """
        return two lists: one containing dictionaries of instantiated problems, the other the parameters used for instantiating 
        """
        problem_list = []
        statement_list = []
        value_list = []

        # make sure new problem is generated
        # by looking up the value_dict in the list of previously generated problems
        while len(statement_list) < num_problems:
            self.instantiate_problem(externals)
            new_problem = self.instantiated_dict

            if new_problem['statement'] not in statement_list or duplicate_ok:
                problem_list.append(self.instantiated_dict)
                statement_list.append(
                    self.instantiated_dict['statement'])
                value_list.append(self.value_dict.copy())

        return problem_list, value_list

    def get_list(self, num_problems: int, externals={}, duplicate_ok=False):
        """
        return a list of num_problems many instantiated problems
        """
        problem_list = []
        statement_list = []

        # make sure new problem is generated
        # by looking up the statement in the list of previously generated problems
        while len(statement_list) < num_problems:
            new_problem = self.get_problem(externals)

            if new_problem.statement not in statement_list or duplicate_ok:
                problem_list.append(new_problem)
                statement_list.append(
                    new_problem.statement)

        return problem_list


class ExpressionParameterProblem(ExpressionProblem, ParameterProblem):

    def get_problem(self, externals={}):
        """
        return a single instantiated problem as Problem

        Returns: Problem

        Keyword arguments:
        externals -- dictionary to be used for parameter evaluation (default {})
        """
        self.instantiate_problem(externals)
        return ExpressionProblem(dict(self.instantiated_dict, **{"title": self.title,
                                                                 "tags": self.tags,
                                                                 "problem_id": self.problem_id}))
