from cyllene2.MathProblems.problem_basic import Problem, MultipleChoice
from cyllene2.MathProblems.problem_instantiator import instantiate_expression
from cyllene2.MathProblems.problem_substitution import substitute_parameter_string


class ParameterProblem(Problem):

    def __init__(
        self,
        problem_id="",
        title="",
        statement="",
        answer="",
        solution="",
        tags=None
    ):

        super().__init__(problem_id, title, statement,
                         answer, solution, tags)

    def instantiate_problem(self, external_parameters):
        """
        instantiate statements, choices, solution
        using dictionary external_parameters
        """

        self.instantiatied_statement = substitute_parameter_string(
            self.statement, **external_parameters
        )

        self.instantiated_solution = substitute_parameter_string(
            self.solution, **external_parameters
        )


class MultipleChoiceParameterProblem(MultipleChoice, ParameterProblem):

    def __init__(self,
                 problem_id="",
                 title="",
                 statement="",
                 choices=None,
                 solution="",
                 tags=None):

        super(MultipleChoice, self).__init__(problem_id, title, statement,
                                             choices, solution, tags)

    def instantiate_problem(self, external_parameters):

        super().instantiate_problem(external_parameters)

        if not isinstance(self.choices, list):
            self.choices = [self.choices]

        self.instantiated_choices = []
        for choice in self.choices:
            if isinstance(choice, str):
                # if answer is a string, try to substitute parameters
                self.instantiated_choices += [substitute_parameter_string(
                    choice, **external_parameters)]
            else:
                # otherwise try to instantiate value
                self.instantiated_choices += [instantiate_expression(
                    choice, **external_parameters)]

        if len(self.instantiated_choices) > 0:
            self.correct_answer = self.instantiated_choices[0]
