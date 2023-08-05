import random
from re import M
from sympy import Basic
from ..aux.helpers import extract_dict, set_attr_dict, get_attr_dict
from ..MathFunctions.math_compare import compare_functions
from ..MathFunctions.math_define import define_expression


class Problem:
    """
    Defines class for basic problem handling: statement, type, answer
    and checking

    attributes:
        name (string): problem name
        statement (string): general statement of the problem, such as
            "Find the derivative of ..."
        solution (string, optional)
    """

    def __init__(self, my_dict={}):

        self.set_core_attributes()

        self.keys = ["statement", "answer",
                     "problem_id", "solution", "solution_title", "tags", "title"]

        if isinstance(my_dict, dict) and dict != {}:
            self.load_dict(my_dict)

    def set_core_attributes(self):

        self.problem_id = ""
        self.title = ""
        self.statement = ""
        self.answer = ""
        self.solution = ""
        self.solution_title = ""
        self.tags = []
        self.flags = {}

    def load_dict(self, my_dict):

        # sanitize my_dict to include only official class keys
        my_dict = extract_dict(my_dict, self.keys)

        # set attributes as given in dictionary
        set_attr_dict(self, my_dict)

    def get_dict(self, keys=[]):

        # sanitize keys to include only official class keys
        keys = list(set(keys).intersection(self.keys))

        return get_attr_dict(self, keys)

    def check_answer(self, answer_string):

        return self.answer == answer_string

    @property
    def has_solution(self):
        return bool(self.solution)


class MultipleChoice(Problem):

    def __init__(self, my_dict={}):

        self.keys = ["statement", "answer",
                     "problem_id", "solution", "solution_title",
                     "tags", "title", "choices"]

        self.problem_id = ""
        self.title = ""
        self.statement = ""
        self.answer = ""
        self.solution = ""
        self.solution_title = ""
        self.tags = []
        self.flags = {}
        self.choices = []

        if isinstance(my_dict, dict) and my_dict != {}:
            self.load_dict(my_dict)

        # Make sure choices is always a list
        if not isinstance(self.choices, list):
            self.choices = [self.choices]

        # shuffle answers and store them in a separate list
        self.shuffle_answers()

    @property
    def num_choices(self):
        return len(self.choices)

    def load_dict(self, my_dict):

        super().load_dict(my_dict)

        # Make sure choices is always a list
        if not isinstance(self.choices, list):
            self.choices = [self.choices]

        if len(self.choices) > 0:
            self.answer = str(self.choices[0])

    # def shuffle_choices(self):

    #     shuffled_choices = self.choices
    #     return random.shuffle(shuffled_choices)

    def shuffle_answers(self):
        self.indices = [i for i in range(self.num_choices)]
        random.shuffle(self.indices)
        self.correct = self.indices.index(0)


class ExpressionProblem(Problem):

    @property
    def answer_expression(self):
        # try to convert answer to sympy expression
        return define_expression(self.answer)[0]

    def check_answer(self, user_answer: str, mode="full"):

        user_answer_expression = define_expression(user_answer)[0]

        if user_answer_expression:
            # user_answer is sympy expression, proceed with check routine
            check = compare_functions(
                user_answer_expression, self.answer_expression, mode)
            if isinstance(check, bool):
                return check
            else:
                print("Unable to decide answer")
                return None

        else:
            print("Invalid answer format")
            return None
