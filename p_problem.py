import f_define as fd
import f_compare as fc

import j_problem as jpr


# # Reserve some (real-valued) symbols in Sympy
# a, b, c, d, p, q, r, s, t, w, x, y, z = sp.symbols(
#     'a b c d p q r s t w x y z', real=True)

# MYLOCALS = {'a': a, 'b': b, 'c': c, 'd': d, 'p': p, 'q': q, 'r': r,
#             's': s, 't': t, 'w': w, 'x': x, 'y': y, 'z': z}





"""
Defines a class for basic problem handling: statement, type, answer
and checking
"""
class Problem():
    """
    attributes:
        name (string): problem name
        statement (string): general statement of the problem, such as
            "Find the derivative of the following function."
        expression (Function, or array of): mathematical expression to 
            be used in problem. 
            Example: 3x^2-1
            (array of) string(s) containing the problem description
        answer_type: type of answer expected
            possible: expression, numerical, boolean, string
        correct_answer: sympy expression
        current_answer: current answer on record
        status (const string): current status of the problem
            'correct', 'incorrect', 'undecided'
    """

    def __init__(self,
                 name,
                 statement, 
                 num_inputs,
                 expression, 
                 answer_type, 
                 correct_answer,
                 eval_mode='full',
                 regen=False
                ):

        self.name = name
        self.statement = statement

        self.num_inputs = num_inputs

        if type(expression) != list:
            expression = [expression]
        self.expression = expression

        self.answer_type = answer_type

        if type(correct_answer) != list:
            correct_answer = [correct_answer]
        self.correct_answer = correct_answer
        
        
        if answer_type == 'numerical' and eval_mode=='full':
            # set right eval level for numerical answers
            self.eval_mode = 'symbolic'
        else:
            self.eval_mode = eval_mode
            
        self.regen = regen
        
        self.status = 'undecided'

        self.current_answer = ['']

        self.check = []

    
    def check_answer(self, answer):
        """
        Checks whether answer is a correct expression
        and if so, compare answer to correct_answer depending on answer_type
        """
        self.check = []
        
        if not isinstance(answer, list):
            answer = [answer]

        if len(answer) < self.num_inputs:
            for i in range(self.num_inputs-len(answer)):
                answer.append('') 

        self.current_answer = [fd.define_expression(answer[i], eval_mode=False)
                            for i in range(self.num_inputs)]

        for i in range(self.num_inputs):
            """
            Check which inputs are syntax ok
            If ok, check answer
            """
            if self.current_answer[i][0] != None:
                
                if self.answer_type == 'expression':
                    self.check.append(
                        fc.compare_functions(self.current_answer[i][0], self.correct_answer[i], mode=self.eval_mode))
                else:
                    self.check.append(
                        fc.compare_functions(self.current_answer[i][0], self.correct_answer[i], mode=self.eval_mode))
            else:
                self.check.append(False)

        self.show_result()


    def state_problem(self):
        jpr.state_problem(self.name, self.statement, self.expression, self.regen)

    def show_result(self):
        jpr.show_result(self.current_answer, self.check)


