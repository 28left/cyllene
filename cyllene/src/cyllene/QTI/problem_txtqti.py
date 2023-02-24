# import os
# import subprocess
import re

from ..MathProblems.problem_basic import MultipleChoice


class Problems2Text:

    letters = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, problems, with_solution=True):

        self.problems = problems
        self.txt_quiz = ""
        self.with_solution = with_solution

    # def output_quiz_markdown_file(self, problem_list, title=None, description=None ,shuffle_answers=False, show_answer=False, one_question_at_time=False, path=None, file_name=None):
    #     if not path:
    #         path = './'
    #     if not file_name:
    #         file_name = 'qtiMarkdown'
    #     complete_path = os.path.join(path, file_name+'.txt')

    #     quiz_string = self.make_quiz(problem_list, title, description, shuffle_answers, show_answer, one_question_at_time)
    #     file = open(complete_path, "w")
    #     file.write(quiz_string)
    #     file.close()

    def make_text_quiz(self,
                       title=None,
                       description=None,
                       shuffle_answers=True,
                       show_answer=False,
                       one_question_at_time=False):

        if title is not None:
            self.txt_quiz += "Quiz title: {}\n".format(title)

        if description is not None:
            self.txt_quiz += "Quiz description: {}\n".format(description)

        if shuffle_answers:
            self.txt_quiz += "Shuffle answers: true\n"

        if show_answer:
            self.txt_quiz += "Show correct answers: true\n"

        if one_question_at_time:
            self.txt_quiz += "One question at a time: true\n"

        for index, problem in enumerate(self.problems):
            formatted_problem = self.convert_multiple_choice_problem(problem)
            if problem.problem_id:
                self.txt_quiz += "Title: " + str(problem.problem_id) + \
                    " (" + str(index+1) + ") \n"
            self.txt_quiz += "{}. ".format(index + 1)
            self.txt_quiz += formatted_problem
            self.txt_quiz += "\n"

            # If ever encounter a spot to put the version number (say, for referencing .png files, replace with index+1)
            version_pattern = re.compile(r"VERSIONGOESHERE")
            self.txt_quiz = version_pattern.sub(str(index+1), self.txt_quiz)

    def convert_multiple_choice_problem(self, problem):

        if self.with_solution:
            return self.format_problem_statement(problem) + \
                self.format_solution(problem) + \
                self.format_multiple_choices(problem)
        else:
            return self.format_problem_statement(problem) + \
                self.format_multiple_choices(problem)

    # def get_problem_type(self, problem: Problem):
    #     return problem.problem_type

    def format_problem_statement(self, problem):

        return problem.statement + "\n"

    def format_solution(self, problem):

        return "... " + problem.solution + "\n"

    def format_multiple_choices(self, problem: MultipleChoice):
        formatted_choices = ""
        for i in range(len(problem.choices)):
            is_answer = (i == 0)
            if is_answer:
                formatted_choices += "*{}) {}\n".format(
                    self.letters[i], problem.choices[i])
            else:
                formatted_choices += "{}) {}\n".format(
                    self.letters[i], problem.choices[i])

        return formatted_choices

    # def make_QTI_quiz(self):

    #     cmd = ['pandoc', '-f', 'markdown', '-o', str(solutions_path)]

    #     proc = subprocess.run(
    #                         cmd,
    #                         input=solutions_text,
    #                         capture_output=True,
    #                         check=True,
    #                         encoding='utf8'
    #                     )

    #     self.qti_quiz = make_text_quiz(self,
    #               problems_list,
    #               title=None,
    #               description=None,
    #               shuffle_answers=False,
    #               show_answer=False,
    #               one_question_at_time=False)
