import ipyvuetify as v
import ipywidgets as w
from ..MathProblems.problem_basic import MultipleChoice
from ..MathProblems.problem_parametermultchoice import MultipleChoiceParameterProblem
from IPython.display import display, clear_output

import random


class VueMultipleChoice(MultipleChoice):

    def assign_problem(self):

        self.display_statement = self.statement
        self.display_choices = self.choices
        self.display_solution = self.solution

    def create_widget(self):

        # Shuffle answers
        indices = [i for i in range(self.num_choices)]
        random.shuffle(indices)
        self.correct = indices.index(0)

        # # Define CSS properties to make text larger
        # display(HTML("<style>.large_font { font-size: 100% }</style>"))
        # display(HTML("<style>.xlarge_font { font-size: 120% }</style>"))

        # store the statement in a widget
        self.vue_statement_widget = w.HTMLMath(
            value="<h2>"+self.display_statement+"</h2>")

        # # enlarge text
        # self.vue_statement.add_class("xlarge_font")

        # Create labels for each answer choice
        vue_answers = [w.HTMLMath(value=self.display_choices[indices[i]])
                       for i in range(self.num_choices)]

        # # Enlarge text for labels
        # for a in answers:
        #     a.add_class("large_font")

        # Create radio buttons with answers as labels (slots)
        self.vue_choices = v.RadioGroup(
            v_model=None,
            children=[
                v.Radio(v_slots=[{
                    'name': 'label',
                    'children': [a]}]) for a in vue_answers]
        )

        # Create a submit button
        self.vue_check_button = v.Btn(
            color='primary', children=['Check Answer'])

        # When check button is clicked, check the currently selected answer
        self.vue_check_button.on_event("click", self.on_click_submit)

        # Create a feedback area
        self.vue_feedback = w.Output()

    def on_click_submit(self, widget, event, data):

        with self.vue_feedback:
            clear_output()

            if self.vue_choices.v_model == self.correct:
                display(v.Alert(text=True, style_='width: 300px',
                        type='success', children=['Correct!']))
                return True
            else:
                display(v.Alert(text=True, style_='width: 300px', type='error',
                        children=['Incorrect!']))
                return False

    def show_problem(self):

        # show statement
        display(self.vue_statement_widget)

        # put answer radio buttons, submit button, and feedback area into a container and show
        con = v.Container(
            children=[self.vue_choices, self.vue_check_button])
        display(con)

        display(self.vue_feedback)


class vueMultipleChoiceParameterProblem(VueMultipleChoice, MultipleChoiceParameterProblem):

    def assign_problem(self, externals={}):

        print("assigning problems...")

        self.instantiate_problem(externals)
        self.display_statement = self.instantiated_statement
        self.display_choices = self.instantiated_choices
        self.display_solution = self.instantiated_solution

    def create_widget(self):

        super().create_widget()

        # Create "New" Button
        self.vue_new_button = v.Btn(
            color='success', children=['New'])

        # When check button is clicked, check the currently selected answer
        self.vue_new_button.on_event("click", self.make_new_problem)

        # Create a dynamic output area for the widget
        self.quiz_widget = w.Output()

    def make_new_problem(self, widget, event, data):

        self.assign_problem()
        self.show_problem()

    def show_problem(self):

        display(self.quiz_widget)

        with self.quiz_widget:
            clear_output()

            # show statement
            display(self.vue_statement_widget)

            # put answer radio buttons, submit button, and feedback area into a container and show
            con = v.Container(
                children=[self.vue_choices, self.vue_check_button, self.vue_new_button])
            display(con)

            display(self.vue_feedback)
