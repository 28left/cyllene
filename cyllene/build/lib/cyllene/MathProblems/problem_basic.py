import random
from ..aux.helpers import extract_dict, set_attr_dict, get_attr_dict


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
                     "problem_id", "solution", "tags", "title"]

        if isinstance(my_dict, dict) and dict != {}:
            self.load_dict(self, my_dict)

    def set_core_attributes(self):

        self.problem_id = ""
        self.title = ""
        self.statement = ""
        self.answer = ""
        self.solution = ""
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


class MultipleChoice(Problem):

    def __init__(self, my_dict={}):

        self.keys = ["statement", "answer",
                     "problem_id", "solution",
                     "tags", "title", "choices"]

        self.problem_id = ""
        self.title = ""
        self.statement = ""
        self.answer = ""
        self.solution = ""
        self.tags = []
        self.flags = {}
        self.choices = []

        if isinstance(my_dict, dict) and my_dict != {}:
            self.load_dict(my_dict)

        # Make sure choices is always a list
        if not isinstance(self.choices, list):
            self.choices = [self.choices]

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

    def shuffle_choices(self):

        shuffled_choices = self.choices
        return random.shuffle(shuffled_choices)


# class ExpressionProblem(Problem)
