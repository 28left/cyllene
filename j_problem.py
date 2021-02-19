from IPython.display import display, Markdown, Latex, Math, clear_output

from sympy import latex

# import f_functionclass as ff
# import f_compare as fc


# def check_problem_text(solution, answer):

#     processed_answer = ff.Function(answer)

#     if processed_answer.is_defined:

#         display(Markdown('You entered: $' + processed_answer.tex_form + '$'))

#         check = fc.compare_functions(solution, processed_answer.sym_form)    
        
#         if check == True:
#             display(Markdown('*Correct*!'))
#         else:
#             display(Markdown('*Please try again.*'))

#     else:

#         display(Markdown('Invalid input'))

#         issues_report=''.join(['\t' + str(i+1) + '. ' + processed_answer.issues[i]+'\n' \
#             for i in range(len(processed_answer.issues))])
#         display(Markdown('Problems encountered:\n' + issues_report))

def state_problem(name, statement, expression, regen=False):
    
    if regen:
        title = '## <font color=\'SteelBlue\'>!! ' + name + '</font>'
    else:
        title = '## ' + name 
    display(Markdown(title))
    display(Markdown(statement))
    if len(expression) > 0:
        for i in range(len(expression)):
            display(Math(latex(expression[i])))


def show_result(processed_answer, check):

    for i in range(len(processed_answer)): 
        if processed_answer[i][0] != None:
            display(Markdown("You entered: $\displaystyle " + latex(processed_answer[i][0]) + "$"))
            if check[i]: 
                display(Markdown('Correct!'))
            else:
                display(Markdown('Incorrect'))

        else:
            display(Markdown('Invalid input.'))
            issues_report=''.join(['\t' + str(j+1) + '. ' + processed_answer[i][1][j]+'\n' \
                for j in range(len(processed_answer[i][1]))])
            display(Markdown('Problems encountered:\n' + issues_report))



