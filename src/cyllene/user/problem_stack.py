from ..aux.helpers import extract_dict


class ProblemStack:
    """
    ProblemStack: class to keep a dictionary of problems used in the current notebook

    attributes:
        stack: dict
    """

    def __init__(self):
        self.stack = {}
        self.user_funcs = {}

    def add(self, problem, name=""):
        if name != "":
            self.stack[name] = problem
        else:
            self.stack[str(problem.problem_id)] = problem

    def get(self, name: str):
        if name in self.stack.keys():
            return self.stack[name]
        else:
            return None

    def update_user_funcs(self):
        # if ipython environment, add user vars to dictionary
        try:
            ip = get_ipython()
            global_dict = ip.user_ns
            user_vars = ip.run_line_magic("who_ls", "")
            self.user_funcs = extract_dict(global_dict, user_vars)
        except NameError:
            pass


# create problem stack
ProbStack = ProblemStack()
