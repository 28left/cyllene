from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets
import random
import markdown
from ..MathProblems.problem_basic import Problem, MultipleChoice
from .widgets_aux import update_output_widget
"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""

COLORS = ['primary', 'success', 'info', 'warning', 'danger']


class ProblemWidget:
    """
    Show a basic widget displaying title and statement
    """

    def __init__(self, problem: Problem):

        self.problem = problem
        self.status = 'undecided'
        self.check = []
        self.title = widgets.Output()
        self.statement = widgets.Output()

        self.has_solution = bool(self.problem.solution)
        self.solution_text = widgets.Output()
        with self.solution_text:
            display(widgets.HTMLMath(markdown.markdown(self.problem.solution)))

        self.solution = widgets.Accordion(
            children=[self.solution_text])
        self.solution.selected_index = None
        self.solution.set_title(0, 'Show Solution')

    def show(self):

        # Show just title and statement
        update_output_widget(self.title, '### ' + self.problem.title)
        update_output_widget(
            self.statement, self.problem.statement)

        display(widgets.VBox([self.title, self.statement]))
        display(self.solution)


class MultipleChoiceWidget(ProblemWidget):

    def __init__(self, problem: MultipleChoice):

        super().__init__(problem)

        self.choices = widgets.Output()
        self.feedback = widgets.Output(layout=widgets.Layout(height='50px'))

        self.shuffle_answers()

        # create buttons
        self.choice_buttons = [
            widgets.Button(
                description='( '+str(i+1)+' )',
                disabled=False,
                button_style=COLORS[i],
                tooltip='Answer choice '+str(i+1),
                layout=widgets.Layout(flex='1 1 auto', width='auto'))
            for i in range(self.problem.num_choices)]

        # Activate handler for every button
        for button in self.choice_buttons:
            # link to a click event function
            button.on_click(self.on_button_clicked)

    def shuffle_answers(self):
        self.indices = [i for i in range(self.problem.num_choices)]
        random.shuffle(self.indices)
        self.correct = self.indices.index(0)

    def show(self):

        # show title and statement
        update_output_widget(self.title, '### ' + self.problem.title)
        update_output_widget(self.statement, self.problem.statement)
        display(widgets.VBox([self.title, self.statement]))

        # display choices
        with self.choices:
            clear_output()
            for i in range(self.problem.num_choices):
                display(widgets.HTMLMathL(markdown.markdown(
                    '**(' + str(i+1) + ')**  &nbsp;&nbsp;  ' + self.problem.choices[self.indices[i]])))

        display(widgets.VBox([self.choices, widgets.HBox(
            self.choice_buttons), self.feedback]))

        with self.feedback:
            clear_output()
            display(Markdown('Please select your answer.'))

        display(self.solution)

    def on_button_clicked(self, bt):

        self.check_answer(bt.description[2:-2])

    def check_answer(self, answer):

        # reset current answer check
        self.check = []

        # Pre-process answer string to remove parentheses (if present)
        answer = answer[0]
        if len(answer) > 0 and answer[0] == '(':
            answer = answer[1:]
        if len(answer) > 0 and answer[-1] == ')':
            answer = answer[:-1]

        try:
            if self.correct == int(answer)-1:
                self.check.append(True)
            else:
                self.check.append(False)
        except ValueError:
            self.check.append('Error')

        if self.check[0] == True:
            result_string = 'You selected: ('+answer+') -- ' + \
                '&#9989; &nbsp; **Correct!**'
            self.status = 'correct'
        elif self.check[0] == False:
            result_string = 'You selected: ('+answer+') -- ' + \
                '&#10060; &nbsp; **Incorrect**'
            self.status = 'incorrect'
        else:
            result_string = 'Please enter an integer value.'
            self.status = 'undecided'

        # show feedback
        with self.feedback:
            clear_output()
            display(Markdown(result_string))
