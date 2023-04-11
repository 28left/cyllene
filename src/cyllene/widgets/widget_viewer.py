from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets
import markdown
from ..MathProblems.problem_handler import ProblemHandler
from ..MathProblems.problem_basic import MultipleChoice
from ..MathProblems.problem_parameter import ParameterProblem
from ..MathProblems.problem_parametermultchoice import MultipleChoiceParameterProblem
from .widgets_aux import update_output_widget
"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""

COLORS = ['primary', 'success', 'info', 'warning', 'danger']


class WidgetViewer:
    """
    Pass a ProblemHandler instance and create a viewer using corresponding widgets
    """

    def __init__(self, problem: ProblemHandler):

        self.problem = problem
        self.problem.select_current_problem()

        # initialize output widgets for various areas
        self.title = widgets.Output()
        self.statement = widgets.Output()
        self.user_answer_area = widgets.Output()
        self.button_area = widgets.Output()
        self.feedback = widgets.Output(layout=widgets.Layout(height='50px'))
        self.solution_text = widgets.Output()
        self.solution_area = widgets.Accordion(children=[self.solution_text])

        self.new_button = widgets.Button(description='New Version',
                                         disabled=False)
        self.new_button.on_click(self.new_button_clicked)

    def new_button_clicked(self, bt):

        self.problem.select_current_problem()

        # update display
        self.build_problem_widget()

    def build_title(self):
        update_output_widget(self.title, '### ' +
                             self.problem.current_problem.title)

    def build_statement(self):
        update_output_widget(
            self.statement, self.problem.current_problem.statement)

    def build_solution(self):
        with self.solution_text:
            clear_output()
            display(widgets.HTMLMath(
                    markdown.markdown(self.problem.current_problem.solution)))

        self.solution_area.selected_index = None
        self.solution_area.set_title(0, 'Show Solution')

    def build_user_answer(self):

        if isinstance(self.problem.current_problem, MultipleChoice):
            self.problem.current_problem.shuffle_answers()
            with self.user_answer_area:
                clear_output()

                for i in range(self.problem.current_problem.num_choices):
                    display(widgets.HTMLMath(
                        value='<b>( ' + str(i+1) + ' )</b>  &nbsp;&nbsp;  ' + self.problem.current_problem.choices[self.problem.current_problem.indices[i]] + "&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;"))

    def build_choice_buttons(self):

        # create buttons
        self.choice_buttons = [
            widgets.Button(
                description='( '+str(i+1)+' )',
                disabled=False,
                button_style=COLORS[i],
                tooltip='Answer choice '+str(i+1),
                layout=widgets.Layout(flex='1 1 auto', width='auto'))
            for i in range(self.problem.current_problem.num_choices)]

        # Activate handler for every button
        for button in self.choice_buttons:
            # link to a click event function
            button.on_click(self.on_choice_button_clicked)

        # display buttons in button area widget
        with self.button_area:
            clear_output()
            display(widgets.HBox(self.choice_buttons))

    def on_choice_button_clicked(self, bt):

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
            if self.problem.current_problem.correct == int(answer)-1:
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

    def build_problem_widget(self):

        # build widgets and add to widget list depending on current problem type
        self.build_title()
        self.widget_list = [self.title]

        if self.problem.regenerates:
            self.widget_list.append(self.new_button)

        self.build_statement()
        self.widget_list.append(self.statement)

        self.build_user_answer()
        self.widget_list.append(self.user_answer_area)

        if isinstance(self.problem.current_problem, MultipleChoice):
            self.build_choice_buttons()
            self.widget_list.append(self.button_area)

        with self.feedback:
            clear_output()
            display(Markdown('Please select your answer.'))
        self.widget_list.append(self.feedback)

        if self.problem.current_problem.has_solution:
            self.build_solution()
            self.widget_list.append(self.solution_area)

    def show(self):
        self.build_problem_widget()
        display(widgets.VBox(self.widget_list))
