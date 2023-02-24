from pyparsing import Suppress
import re


def prepare_tex(unprepared: str) -> str:
    """if possible, produce string in latex format appropriate for sympy's parse_latex()"""

    # remove outer \[...\]
    latex_pattern = Suppress("\[") + ... + Suppress("\]")
    unprepared = r"{}".format(latex_pattern.parseString(unprepared)[0])

    # remove certain keywords unrecognizable to sympy's parse_latex command
    literals = ['\left', '\\right', '\mathrm', '\mathbb',
                '\mathbf', '\mathit', '\\textbf', '\\textit', '\\texttt']
    for literal in literals:
        unprepared = unprepared.replace(literal, '')

    # any of these operators should not be nested in curly braces
    iterated_operators = ['\sum', '\int', '\bigcup', '\bigcap']
    for iterated_operator in iterated_operators:
        unprepared = unprepared.replace(
            "{" + iterated_operator + "}", iterated_operator)

    # any differentials for integrals should not be nested in curly braces
    unprepared = re.sub(r"({)(d.*?)(})", r"\2", unprepared)
    return unprepared
