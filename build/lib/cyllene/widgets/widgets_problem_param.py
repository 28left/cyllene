from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets
from ..MathProblems.problem_parameter import ParameterProblem

from .widgets_problem_basic import ProblemWidget, MultipleChoiceWidget
from .widgets_aux import update_output_widget

"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""

COLORS = ['primary', 'success', 'info', 'warning', 'danger']


class ParameterProblemWidget(ProblemWidget):
    """
    Show a basic widget displaying title and statement
    """

    def __init__(self, problem: ParameterProblem):

        self.param_problem = problem
        super().__init__(self.param_problem.get_problem())

        self.problem_area = widgets.Output()
        # layout={'border': '1px dotted gray'})
        self.new_button = widgets.Button(description='New Version',
                                         disabled=False)
        self.new_button.on_click(self.new_button_clicked)

    def show(self):

        update_output_widget(self.title, '### ' + self.problem.title)
        display(widgets.VBox([self.title, self.new_button]))

        update_output_widget(self.problem_area, self.problem.statement)
        display(self.problem_area)

        display(self.solution)

    def new_button_clicked(self, bt):

        self.problem = self.param_problem.get_problem()
        update_output_widget(self.problem_area, self.problem.statement)


class MultipleChoiceParameterWidget(ParameterProblemWidget, MultipleChoiceWidget):

    def show(self):

        update_output_widget(self.title, '### ' + self.problem.title)
        display(widgets.VBox([self.title, self.new_button]))

        self.update_problem_area()
        display(self.problem_area)

        with self.feedback:
            clear_output()
            display(Markdown('Please select your answer.'))

        display(widgets.VBox(
            [widgets.HBox(self.choice_buttons), self.feedback, self.solution]))

    def update_problem_area(self):

        with self.problem_area:
            clear_output()
            display(Markdown(self.problem.statement))

            for i in range(self.problem.num_choices):
                display(Markdown('**(' + str(i+1) + ')**  &nbsp;&nbsp;  ' +
                                 self.problem.choices[self.indices[i]]))

    def new_button_clicked(self, bt):

        self.shuffle_answers()
        self.problem = self.param_problem.get_problem()
        self.update_problem_area()
        with self.feedback:
            clear_output()
        self.solution.selected_index = None
        update_output_widget(self.solution_text, self.problem.solution)
