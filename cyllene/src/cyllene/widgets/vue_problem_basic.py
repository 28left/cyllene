from unittest.loader import VALID_MODULE_NAME
from IPython.display import display, clear_output
import time

import ipywidgets as widgets
import ipyvuetify as vuew

from py_asciimath.translator.translator import ASCIIMath2Tex
from sympy.parsing.latex import parse_latex

from .widgets_problem_basic import ProblemWidget
from ..MathProblems.problem_basic import Problem, MultipleChoice, ExpressionProblem

from .widgets_aux import update_output_widget, shuffle_answers
from ..aux.input_transform import prepare_tex

"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""

# COLORS = ['primary', 'success', 'info', 'warning', 'danger']


class VueProblemWidget(ProblemWidget):
    """
    Show a basic widget displaying title and statement
    """

    def __init__(self, problem: Problem):

        super().__init__(problem)

        # create a solution text button
        self.solution_btn = vuew.Btn(
            color='indigo',
            text=True,
            children=["Solution"])

        # create solution dropdown button
        self.solution_icn = vuew.Btn(
            color='indigo',
            # class_='mx-2 indigo lighten-3',
            icon=True,
            children=[vuew.Icon(children=['mdi-chevron-down'])])

        # redefine solution as vue container
        self.solution = vuew.Container(
            children=[self.solution_text])
        self.solution_show = False
        self.solution.hide()
        self.solution_btn.on_event("click", self.on_click_solution)
        self.solution_icn.on_event("click", self.on_click_solution)

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

    def show(self):
        # Show just title and statement
        update_output_widget(self.title, '### ' + self.problem.title)
        update_output_widget(self.statement, self.problem.statement)

        display(vuew.Card(
            class_="mx-auto",
            width="600",
            children=[
                vuew.CardTitle(children=[self.problem.title]),
                vuew.CardText(children=[self.statement]),
                vuew.CardActions(
                    children=[
                        self.solution_btn,
                        vuew.Spacer(),
                        self.solution_icn]),
                self.solution
            ]
        ))

        # display(widgets.VBox([self.title, self.statement]))
        # display(vuew.Container(children=[self.solution_btn, self.solution]))


class VueMultipleChoiceWidget(VueProblemWidget):

    def __init__(self, problem: MultipleChoice):

        super().__init__(problem)

        # Create a submit button
        self.check_btn = vuew.Btn(
            class_='mx-2 teal lighten-3',
            width="150",
            children=["Check Answer"])

        # When check button is clicked, check the currently selected answer
        self.check_btn.on_event("click", self.on_click_submit)

        # show solution button is initially disabled (until answer is submitted)
        self.solution_btn.disabled = True
        self.solution_icn.disabled = True

        # shuffle choices
        self.indices, self.correct = shuffle_answers(self.problem.num_choices)

        # create radio buttons
        self.create_radio_buttons()

        self.choice_sheet = vuew.Sheet(
            children=[vuew.Container(children=[self.vue_choices])])

        # # create a feedback alerts
        # self.feedback_incorrect = vuew.Alert(
        #     type="error", dense=True, children=["Incorrect, please select another answer."])
        # self.feedback_incorrect.hide()
        # self.feedback_correct = vuew.Alert(
        #     type="success", dense=True, children=["Correct!"])
        # self.feedback_correct.hide()
        # self.feedback = vuew.Container(
        #     children=[self.feedback_incorrect, self.feedback_correct])

    def create_radio_buttons(self):

        # Create labels for each answer choice
        self.vue_answers = [widgets.HTMLMath(
            value=self.problem.choices[self.indices[i]]) for i in range(self.problem.num_choices)]

        # Create little feedback icons
        self.vue_answer_feedback = [vuew.Icon(
            color="red",
            children=["mdi-close"])
            for i in range(self.problem.num_choices)]

        # Correct answer icon is check symbol
        self.vue_answer_feedback[self.correct] = vuew.Icon(
            color="green",
            children=["mdi-check"])

        # Hide feedback icons initially
        for i in range(self.problem.num_choices):
            self.vue_answer_feedback[i].hide()

        # Create radio buttons for quiz with answer text in slots
        self.radios = [
            vuew.Radio(v_slots=[{
                'name': 'label',
                'children': [self.vue_answers[i], self.vue_answer_feedback[i]]}]) for i in range(self.problem.num_choices)]

        # Put radio buttons in group
        self.vue_choices = vuew.RadioGroup(
            v_model=None,
            children=self.radios
        )

    def show(self):

        # show title and statement
        update_output_widget(self.title, '### ' + self.problem.title)
        update_output_widget(self.statement, self.problem.statement)
        display(widgets.VBox([self.title, self.statement]))

        # Put choices and feedback in a flex container
        # display(vuew.Html(tag='div', class_='d-flex align-center',
        #                   children=[
        #                       vuew.Container(children=[self.vue_choices]),
        #                       self.feedback]))
        display(self.choice_sheet)

        # Show check and solution buttons
        display(vuew.Container(
            children=[self.check_btn, self.solution_btn, self.solution_icn]))
        display(self.solution)

    def on_click_submit(self, widget, event, data):

        # with self.feedback:
        #     clear_output()

        # if nothing is selected, return
        if self.vue_choices.v_model == None:
            return None

        # enable show solution button
        self.solution_btn.disabled = False
        self.solution_icn.disabled = False
        self.vue_answer_feedback[self.vue_choices.v_model].show()

        self.choice_sheet.color = ""
        time.sleep(0.1)

        # get selected button and compare with correct index
        if self.vue_choices.v_model == self.correct:
            # display(vuew.Alert(text=True, style_='width: 300px',
            #         type='success', children=['Correct!']))
            # self.feedback_correct.show()
            # self.feedback_incorrect.hide()
            self.choice_sheet.color = "green lighten-5"
            return True
        else:
            self.radios[self.vue_choices.v_model].disabled = True
            # display(vuew.Alert(text=True, style_='width: 300px', type='error',
            #         children=['Incorrect!']))
            # self.feedback_correct.hide()
            # self.feedback_incorrect.show()
            self.choice_sheet.color = "red lighten-5"
            return False


class VueExpressionWidget(VueProblemWidget):
    """
    Show a basic widget displaying title and statement
    """

    def __init__(self, problem: ExpressionProblem):

        super().__init__(problem)

        # Create a text field and a display field for the processed input
        self.entry = vuew.TextField(
            label='Answer',
            outlined=True,
            clearable=True,
            placeholder='Enter your answer as MathAscii, e.g., sqrt(x)/x^3', v_model="")
        self.processed_display = widgets.HTMLMath(description="You entered: ")

        # Asciimath converter
        self.asciimath2tex = ASCIIMath2Tex(log=False, inplace=True)

        # Create a submit button
        self.check_btn = vuew.Btn(
            class_='mx-2 teal lighten-3',
            width="150",
            children=["Check Answer"])

        # Container for entry and submission
        self.entry_sheet = vuew.Sheet(
            children=[vuew.Container(children=[self.entry, self.processed_display])])

        # When check button is clicked, check the current answer in textfield
        self.check_btn.on_event("click", self.on_click_submit)
        self.check_btn.disabled = True

        # show solution button is initially disabled (until answer is submitted)
        self.solution_btn.disabled = True
        self.solution_icn.disabled = True

    def process_input(self, args):
        """update method for entry component"""
        try:
            # py_asciimath's asciimath2tex command
            tex = self.asciimath2tex.translate(args['new'], displaystyle=True)

            # display "unprepared" tex
            self.processed_display.value = tex

            # prepare tex for sympy's parse_latex
            prepared_tex = prepare_tex(tex)

            # store parse_latex of prepared tex
            # with some substitutions for sympy
            self.user_expr = parse_latex(prepared_tex)

            # allow for submission
            self.check_btn.disabled = False

        except:
            # literal display matching entry
            self.processed_display.value = args['new']

            # no valid sympy expression
            self.user_expr = None

            # prevent submission
            self.check_btn.disabled = True

    def show(self):

        # show title and statement
        update_output_widget(self.title, '### ' + self.problem.title)
        update_output_widget(self.statement, self.problem.statement)
        display(widgets.VBox([self.title, self.statement]))

        display(self.entry_sheet)
        # add a handler when input changes
        self.entry.observe(self.process_input, 'v_model')

        # Show check and solution buttons
        display(vuew.Container(
            children=[self.check_btn, self.solution_btn, self.solution_icn]))
        display(self.solution)

    def on_click_submit(self, widget, event, data):

        # enable show solution button
        self.solution_btn.disabled = False
        self.solution_icn.disabled = False

        self.entry_sheet.color = ""
        time.sleep(0.1)

        check = self.problem.check_answer(self.user_expr)

        # check answer
        if check == True:
            self.entry_sheet.color = "green lighten-5"
            return True
        elif check == False:
            self.entry_sheet.color = "red lighten-5"
            return False
        else:
            self.entry_sheet.color = "gray lighten-5"
            return None
