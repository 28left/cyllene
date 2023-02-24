from ..ProblemParser.parser import parse
from ..ProblemParser.parser_webassign_new import parse_webassign
from ..MathProblems.problem_parametermultchoice import MultipleChoiceParameterProblem
from ..QTI.problem_txtqti import Problems2Text
from ..widgets.widgets_problem_param import MultipleChoiceParameterWidget
import text2qti as t2q


def make_problem(prob_string, externals=None, webassign=False):
    """Generate a problem from a string in Problem format

    :param prob_string: string containing the problem
    :returns: object of Problem class
    :param externals: additional dictionary to be used for instantiation
    :param webassign: Boolean whether to use WebAssign parser instead
    """

    if externals is None:
        externals = {}

    if webassign:
        init_dict = parse_webassign(prob_string)
    else:
        init_dict = parse(prob_string)
    return MultipleChoiceParameterProblem(init_dict, externals)


def make_qti(problem, num_questions: int, solution=False, externals=None):
    """Generate a QTI quiz file from a problem

    :param problem: Multiple Choice Parameter Problem
    :param num_questions: number of questions to be generated
    :param solution: Boolean whether to include solution or not
    :param externals: additional dictionary to be used for instantiation
    :returns: nothing
    """

    # print(num_questions)

    if externals is None:
        externals = {}

    title_string = problem.problem_id+" - "+problem.title
    if not solution:
        title_string += " (no solutions)"
        
    plist = problem.get_list(num_questions, externals)

    qti_problem = Problems2Text(plist, with_solution=solution)

    qti_problem.make_text_quiz(
        title=title_string, shuffle_answers=True)

    # print all questions as txt (for debugging)
    print(qti_problem.txt_quiz)

    # load text2qti config
    config = t2q.Config()
    config.load()

    # text2qti.Quiz object, passing contents of txt file
    quiz = t2q.Quiz(qti_problem.txt_quiz, config=config)
    # text2qti.QTI object (to be written into a .zip)
    qti = t2q.QTI(quiz)
    # write the text2qti.QTI object into .zip
    if solution:
        file_name = problem.problem_id+".zip"
    else:
        file_name = problem.problem_id+"_nosol.zip"

    qti.save(file_name)
    print("QTI file save as "+file_name)


def show_problem(problem: MultipleChoiceParameterProblem):

    MultipleChoiceParameterWidget(problem).show()
