#!/usr/bin/env python
# coding: utf-8
import random
import sys
import sympy as sp

from IPython.display import Markdown


# import custom modules
import f_functionclass as ff
import f_compare as fc
import f_aux as fa
import f_define as fd
import f_random as fr
import f_plots as fpl

import p_problem as pp

import j_problem as jpr

# Suppress long traceback messages and just output error 
ipython = get_ipython()

def exception_handler(exception_type, exception, traceback):
    print("Your input led to an error. You can find more information about the error below.")
    print("%s: %s" % (exception_type.__name__, exception), file=sys.stderr)
    
ipython._showtraceback = exception_handler


# Allow using '^' for exponentiation
def replace_exponentiation_symbol(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.replace('^','**'))
    return new_lines

ipython.input_transformers_cleanup.append(replace_exponentiation_symbol)

  

# Define answer cell magic

from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

@register_cell_magic
def answer(line, cell):
    if cell is None:
        print("Your answer is empty. Please try again.")
        return None
    try:
        problem = problemStack[line]
        answer = cell.rstrip().split('\n')
        problem.check_answer(answer)
    except:
        print("Error")
        
        

# Reserve some (real-valued) symbols in Sympy
a, b, c, d, p, q, r, s, t, w, x, y, z = \
    sp.symbols('a b c d p q r s t w x y z', real=True)

# Reserve some more symbols
k, C, L = sp.symbols('k C L', real=True)

# Reserve standard function symbols
# f, g, h = sp.symbols('f g h', cls=sp.core.function.Function)

# MYLOCALS = {'a': a, 'b': b, 'c': c, 'd': d, 'p': p, 'q': q, 'r': r,
#             's': s, 't': t, 'w': w, 'x': x, 'y': y, 'z': z}


# Basic library of specific functions
RANDOM_FUNCTION_LIST = [
    ['2x+1', 'linear'], ['3x-1', 'linear'], ['(1/2)*x+3', 'linear'],
    ['x+5', 'linear'], ['x-3', 'linear'], ['-x+4', 'linear'],
    ['(1/4)*x-1', 'linear'],
    ['6t', 'linear'], ['2-6t', 'linear'], ['(1/3)*x+2', 'linear'],
    ['(1/4)*x+3', 'linear'], ['(1/5)*x+4', 'linear'], ['(1/6)*x+5', 'linear'],
    ['(1/7)*x+6', 'linear'], ['(1/8)*x+7', 'linear'], ['(1/9)*x+8', 'linear'],
    ['(1/2)*(t**2)', 'quadratic'], ['3*(t**2)+7*t+1', 'quadratic'],
    ['6*(x**2)-8*x+3', 'quadratic'], ['3*(x**2)+5', 'quadratic'],
    ['(2*x+1)^2', 'quadratic'],
    ['(x+3)^2', 'quadratic'], ['(1/6)*(x**2)+1/2', 'quadratic'],
    ['(1/3)*x^2 +2x+1', 'quadratic'], ['(1/4)*(x**2)+2*x+1', 'quadratic'],
    ['(1/5)*(x**2)+4*x', 'quadratic'], ['(1/7)*x^2+3x-2', 'quadratic'],
    ['t**3 + 5*t -12 ', 'cubic'], ['x**3-3*(x**2)+5*x', 'cubic'],
    ['4*(x**3)-2', 'cubic'],
    ['2*(x**3)-3*(x**2)+1', 'cubic'], ['t**3+t', 'cubic'],
    ['t**3-8', 'cubic'], ['-2*x^3-3', 'cubic'], ['-4*x^3+1', 'cubic'],
    ['4*(x**3)+2*x+1', 'cubic'], ['-8*x^3+3*x^2+1', 'cubic'],
    ['y**3-4*y+2', 'cubic'], ['-2*y^3+3', 'cubic'],
    ['7*(x**3)+2*(x**2)', 'cubic'],
    ['x+5', 'increasing'], ['x**3+5', 'increasing'],
    ['2*(x**3)-8', 'increasing'],
    ['2*log(x)', 'increasing'], ['2*x^5-9', 'increasing'],
    ['3*x-3', 'increasing'],
    ['12*x^3-12', 'increasing'], ['7*x-2', 'increasing'],
    ['(1/4)*x-1/2', 'increasing'],
    ['(x-3)^3', 'increasing'], ['-x-2', 'decreasing'],
    ['-x^3+5', 'decreasing'],
    ['-2*log(x)+1', 'decreasing'], ['-2*x-4', 'decreasing'],
    ['-x^7+3', 'decreasing']
]



# create problem stack
problemStack = {} 



"""
User wrappers for various functions
"""


def function(expr):
    """
    Defines a function based on a syntax check
    and a Function object, using lambda operator.
    Returns a pure function.
    """
    func = ff.Function(expr)

    if func.is_defined:
        return lambda x: func.eval_at(x)

    else:
        issues_report=''.join(['\t' + str(i+1) + '. ' + func.issues[i]+'\n' \
            for i in range(len(func.issues))])
        print('Problems encountered:\n' + issues_report)
        return None
        # raise ValueError('Problems encountered:\n'+issues_report)

# def function(expr):
#     [func, issues] = fd.define_function(expr)
#     if issues:
#         print("Invalid format")
#         return None
#     else:
#         return func

def random_function(arg='random'):
    """
    Pick a function at random. 
    One of the folliwing types can be specified:
    'const', 'linear', 'quadratic', 'cubic', 'squareroot',
    'cubicroot', 'rational', 'exp', 'tri', 'log', 'comp',
    'random'
    """
    if arg in ff.FUNCTION_LIST:
        func = ff.Function(arg)
    else:
        func = ff.Function('random')

    return lambda x: func.eval_at(x)
    

def expression(expr):
    """
    Defines a function based on a syntax check
    and a Function object.
    Returns a Sympy object.
    """
    func = ff.Function(expr)

    if func.is_defined:
        return func.sym_form

    else:
        issues_report=''.join(['\t' + str(i+1) + '. ' + func.issues[i]+'\n' \
            for i in range(len(func.issues))])
        print('Problems encountered:\n' + issues_report)
        return None


def compare(expr1, expr2):
    return fc.compare_functions(expr1, expr2)


def check_answer(solution, answer):
    return jpr.check_problem_text(solution, answer)

    
def graph(expr):
    """ Try to find good plotting range and plot the graph """

    var = fa.get_variables(expr)

    try:
        [xran, yran] = fpl.find_plot_range(expr)
        sp.plot(expr, (var[0], xran[0], xran[1]), axis_center=(0,0),
            ylim=(yran[0],yran[1]))
    except:
        sp.plot(expr)

def second_derivative(expr):
    return sp.diff(sp.diff(expr,x),x)