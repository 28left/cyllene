from psucalc import *

# a, b, c, d, p, q, r, s, t, w, x, y, z = \
#     var('a b c d p q r s t w x y z', domain='real')
# # RealNumber = float; Integer = int


P_1 = pp.Problem('Problem 1',
                 'What is the smallest sphenic number?',      
                 1,
                 '',
                 'numerical',
                 [expression(30)]
                 )

# Add problem to stack
problemStack[P_1.name] = P_1

s_2 = sp.sympify('1/6', evaluate=True)

P_2 = pp.Problem('Problem 2',
                 r'What is $\frac{2}{3}-\frac{1}{2}$?',
                 1,
                 '',
                 'numerical',
                 [s_2]
                 )

# Add problem to stack
problemStack[P_2.name] = P_2



P_3 = pp.Problem('Problem 3', r'$ 1.01+0.22 = $ ? ', 1,  '', 'numerical', [expression(1.23)])
problemStack[P_3.name] = P_3

P_4 = pp.Problem('Problem 4', r'Simplify:   $\qquad 5x - 3x$ ', 1,  '', 'expression', [expression('2x')])
problemStack[P_4.name] = P_4

P_5 = pp.Problem('Problem 5', r'Input the fraction $\qquad \dfrac{x+3}{x^2-1}$ ', 1,  '', 'expression', [expression('(x+3)/(x^2-1)')])
problemStack[P_5.name] = P_5


# P_6 = pp.Problem('Problem 6',
#                         r"Solve $ "+ str(coeff[0])+"x+"+str(coeff[1])+" = "+ str(coeff[2])+"$ for $x$.", 
#                         1,
#                         '',
#                         'numerical',
#                         [solution],
#                         regen=True
#                        )
# problemStack[P_6.name] = P_6
# P_6.state_problem()                  )
 
def generate_problem(name, out=True):
    global problemStack

    params = [random.randint(2,6) for i in range(3)]
    sol = sp.sympify(sp.Rational(params[2]-params[1],params[0]), rational=True)

    myProblem = pp.Problem(name,
                        r"Solve $ "+ str(params[0])+"x+"+str(params[1])+" = "+ str(params[2])+"$ for $x$.", 
                        1,
                        '',
                        'numerical',
                        [sol],
                        regen=True
                       )
    problemStack[myProblem.name] = myProblem
    if out:
        myProblem.state_problem()


generate_problem('Problem 6', out=False)
