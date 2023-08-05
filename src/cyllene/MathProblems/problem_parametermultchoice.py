from .problem_basic import MultipleChoice
from .problem_parameter import ParameterProblem
from .problem_instantiator import instantiate_expression
from .problem_substitution import substitute_parameter_string


class MultipleChoiceParameterProblem(MultipleChoice, ParameterProblem):

    def __init__(self, my_dict={}, externals={}):

        super(MultipleChoice, self).set_core_attributes()
        super(ParameterProblem, self).set_core_attributes()

        self.keys = ["statement", "answer", "choices",
                     "problem_id", "solution", "solution_title",
                     "tags", "title", "parameters"]

        if isinstance(my_dict, dict) and my_dict != {}:
            self.load_dict(my_dict)
        if externals:
            self.user_vars = externals

    def instantiate_problem(self, externals={}):

        if externals:
            # update users vars
            self.user_vars.update(externals)

        super().instantiate_problem(self.user_vars)

        self.instantiated_dict["choices"] = []
        for choice in self.choices:
            if isinstance(choice, str):
                # if answer is a string, try to substitute parameters
                self.instantiated_dict["choices"] += [substitute_parameter_string(
                    choice, **(dict(self.user_vars, **self.value_dict)))]
            else:
                # otherwise try to instantiate value
                self.instantiated_dict["choices"] += [instantiate_expression(
                    choice, dict(self.user_vars, **self.value_dict))]

    # def get_instantiated_dict(self):
    #     """return a dictionary just with the instantiated entries"""

    #     return_dict = super().get_instantiated_dict()
    #     return_dict["choices"] = self.instantiated_choices

    #     return return_dict

    # def get_single_dict(self, externals={}):

    #     self.instantiate_problem(externals)
    #     return self.get_instantiated_dict()

    def get_problem(self, externals={}):
        """
        return a single instantiated problem as MultipleChoice

        Returns: Problem

        Keyword arguments:
        external_parameters -- dictionary to be used for parameter evaluation (default {})
        """
        self.instantiate_problem(externals)
        return MultipleChoice(dict(self.instantiated_dict, **{"title": self.title,
                                                              "tags": self.tags,
                                                              "problem_id": self.problem_id,
                                                              "solution_title": self.solution_title}))

    # def get_list(self, num_problems: int, externals={}, duplicate_ok=False):
    #     """return a list of num_problems many instantiated problems"""
    #
    #     problem_list, value_list = self.get_list_dict(
    #         num_problems, externals, duplicate_ok)
    #
    #     plist = [MultipleChoice(problem_list[i]) for i in range(num_problems)]
    #
    #     return plist, value_list
