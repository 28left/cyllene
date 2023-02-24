from unittest.loader import VALID_MODULE_NAME
from IPython.display import display, clear_output, Markdown

import ipyvuetify as vuew
import ipywidgets as widgets
from ..MathProblems.problem_basic import Problem
from .widgets_aux import update_output_widget, shuffle_answers
from .vue_problem_basic import VueProblemWidget, VueMultipleChoiceWidget

"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""

# COLORS = ['primary', 'success', 'info', 'warning', 'danger']


class VueParameterProblemWidget(VueProblemWidget):
    """
    Show a basic widget displaying title and statement
    """

    def __init__(self, problem: Problem):

        self.param_problem = problem
        super().__init__(self.param_problem.get_problem())

        self.problem_area = widgets.Output()

        # Define Vue NEW button
        self.new_button = vuew.Btn(
            class_='mx-2 amber lighten-3',
            children=["New Version"])
        self.new_button.on_event("click", self.new_button_clicked)

    def on_click_solution(self, widget, event, data):

        if self.solution_show:
            self.solution.hide()
            self.solution_icn.children = [vuew.Icon(
                children=['mdi-chevron-down'])]
            # self.solution_btn.class_ = "mx-2 indigo lighten-3"

        else:
            self.solution.show()
            self.solution_icn.children = [
                vuew.Icon(children=['mdi-chevron-up'])]
            # self.solution_btn.class_ = "mx-2 indigo lighten-5"

        self.solution_show = not self.solution_show

    def new_button_clicked(self, widget, event, data):

        self.problem = self.param_problem.get_problem()

        update_output_widget(self.problem_area, self.problem.statement)

        self.solution_show = False
        self.solution.hide()
        self.solution_icn.children = [vuew.Icon(
            children=['mdi-chevron-down'])]

        update_output_widget(self.solution_text, self.problem.solution)

    def show(self):
        # Show just title and statement
        # update_output_widget(self.title, '### ' + self.problem.title)
        # update_output_widget(self.statement, self.problem.statement)

        with self.problem_area:
            clear_output()
            display(Markdown(self.problem.statement))

        display(vuew.Card(
            class_="mx-auto",
            width="600",
            children=[
                vuew.CardTitle(children=[self.problem.title]),
                vuew.CardText(children=[self.problem_area]),
                vuew.CardActions(
                    children=[
                        self.new_button,
                        self.solution_btn,
                        self.solution_icn]),
                self.solution
            ]
        ))

        # display(widgets.VBox([self.title, self.statement]))
        # display(vuew.Container(children=[self.solution_btn, self.solution]))


class VueParameterMultipleChoiceWidget(VueParameterProblemWidget, VueMultipleChoiceWidget):

    def show(self):

        # show title
        update_output_widget(self.title, '### ' + self.problem.title)
        # display(vuew.Container(children=[self.title]))
        display(self.title)

        # Update the radio button statements with the current problem instance
        self.update_problem_area()

        # Put choices and feedback in a flex container
        display(self.statement)
        display(self.choice_sheet)

        # display(vuew.Html(tag='div', class_='d-flex flex-column',
        #                   children=[
        #                       self.problem_area,
        #                       self.feedback]))

        # Show buttons and solution
        display(vuew.Container(
            children=[self.check_btn, self.new_button, self.solution_btn, self.solution_icn]))
        display(self.solution)

    def update_problem_area(self):

        update_output_widget(self.statement, self.problem.statement)

        self.create_radio_buttons()

        self.choice_sheet.color = ""
        self.choice_sheet.children = [
            vuew.Container(children=[self.vue_choices])]

        # with self.problem_area:
        #     clear_output()
        #     display(Markdown(self.problem.statement))
        #     display(self.choice_sheet)

    def new_button_clicked(self, widget, event, data):

        self.problem = self.param_problem.get_problem()

        # Shuffle answer choices
        # create a random order for answers
        self.indices, self.correct = shuffle_answers(self.problem.num_choices)

        self.update_problem_area()

        self.solution_show = False
        self.solution.hide()
        self.solution_icn.children = [vuew.Icon(
            children=['mdi-chevron-down'])]

        update_output_widget(self.solution_text, self.problem.solution)
