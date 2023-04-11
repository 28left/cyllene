import random
# from ..MathProblems.problem_basic import Problem, MultipleChoice
from ..MathProblems.problem_parameter import ParameterProblem
# from ..MathProblems.problem_parametermultchoice import MultipleChoiceParameterProblem
# from .widgets_aux import update_output_widget
"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""


class ProblemHandler:
    """
    Pass a problem instance (or a list thereof) and display it using corresponding widgets
    """

    def __init__(self, problems: list):

        self.problems = problems
        self.status = 'undecided'
        self.check = []
        self.regenerates = False
        self.current_problem = None

        # determine whether several problems are present and whether they regenerate
        if self.has_problem:
            if len(problems) == 1:
                if isinstance(problems[0], ParameterProblem):
                    self.regenerates = True
            else:
                self.regenerates = True

    @property
    def has_problem(self):
        return bool(self.problems)

    def select_current_problem(self):
        if not self.has_problem:
            return

        self.current_problem = random.choice(self.problems)
        if isinstance(self.current_problem, ParameterProblem):
            self.current_problem = self.current_problem.get_problem()
