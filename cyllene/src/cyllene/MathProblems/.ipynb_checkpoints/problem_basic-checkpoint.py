import string


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

    def __init__(
        self,
        problem_id="",
        title="",
        statement="",
        answer="",
        solution="",
        tags=None
    ):

        self.problem_id = problem_id
        self.title = title
        self.statement = statement
        self.answer = answer
        self.solution = solution

        if tags is None:
            self.tags = []

    def load_json(self, json_dict):

        dict_keys = ["statement", "answer",
                     "problem_id", "solution", "tags", "title"]

        for key in dict_keys:
            if key in json_dict.keys():
                setattr(self, key, json_dict[key])


class MultipleChoice(Problem):
    def __init__(
        self,
        problem_id="",
        title="",
        statement="",
        choices=None,
        solution="",
        tags=None
    ):

        if isinstance(choices, list) and len(choices) > 0:
            self.choices = choices
            self.correct_answer = str(choices[0])
        else:
            self.choices = []
            self.correct_answer = ""

        super().__init__(problem_id, title, statement,
                         self.correct_answer, solution, tags=tags)

    def load_json(self, json_dict):

        super().load_json(json_dict)

        if "choices" in json_dict and isinstance(json_dict["choices"], list) and len(json_dict["choices"]) > 0:
            self.choices = json_dict["choices"]
            self.correct_answer = str(self.choices[0])
