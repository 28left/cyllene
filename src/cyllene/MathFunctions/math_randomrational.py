import sympy as sp
import numpy as np
import random

x = sp.Symbol('x', real=True)

"""
## Alternative Approach

Workflow for reliably generating rational functions by building the function with some randomization in a chosen structure. The structure will be broken into two parts: a (generically) irreducible part times a fully reducible part. The irreducible part offers behaviors unachievable by rational functions of the form 

$$\frac{(x - z_1) \cdots (x - z_M)}{(x - a_1) \cdots (x - a_N)},$$

such as the behavior under the rational function $\frac{x^4 + 1}{x^2 + 1}$ (irreducible); whereas the reducible part allows us to guarantee a certain set of zeros and vertical and horizontal asymptotes. 

The following is how we construct our ultimate function `r`:


*Reducible Part*
- Generate `M` $\sim U\{1, ... 6\}$.
- Produce `zeros_and_sings = [...]` by randomly generating $M$ many reals $z_i \sim U[0, 1]$.
- Produce `multiplicities = [...]` by assigning each of the $M$ elements a multiplicity $m_i \in \{-2, -1, 0, 1, 2\}$, randomly selected according to the corresponding probability distribution $\left(\frac{1}{8}, \frac{1}{8}, \frac{1}{2}, \frac{1}{8}, \frac{1}{8} \right)$.
- Produce the `numerator` $\prod\limits_{1 \leq i \leq 6; \; m_i > 0} (x - z_i)^{m_i}$ and `denominator` $\prod\limits_{1 \leq i \leq 6; \; m_i < 0} (x - z_i)^{m_i}$
- Decide a potential horizontal asymptote value by generating random `h` $\sim N(0, 5)$. 
- Conclude the reducible part `red = h * numerator / denominator`

*Irreducible Part*
- Generate degrees `m`, `n` for both the numerator and denominator $\sim U\{0, ..., 5\}$
- Generate `m` and `n` many coefficients $(c_i)_{i = 0, ..., m - 1}$, $(d_i)_{i = 0, ..., n - 1}$ for each part, with each coefficient $\sim U[-5, 5]$.
- Produce `numerator` $x^{m} + \sum_{i = 0}^{m - 1} c_i \cdot x^i$ and `denominator` $x^{n} + \sum_{i = 0}^{n - 1} d_i \cdot x^i$
- Conclude the (generically) irreducible part `irred = numerator / denominator`

*Together*

Set `r = irred * red` 

In reality, we'll have to pass the product of both `numerator`s and the product of both `denominator`s as arguments into the constructor `RatFunction` to produce `r`.
"""

# generate random outcome over provided probability distribution


def discrete_distribution(outcomes, probabilities):
    return outcomes[np.random.choice(len(outcomes), p=probabilities)]

# generate random integer uniformly between lower and upper (inclusive)


def integer_uniform(lower, upper):
    N = upper - lower + 1
    return np.random.choice(N, p=[1 / N for i in range(N)]) + lower


def get_reducible():
    # number of zeros and singularities in the reducible part
    M = integer_uniform(1, 4)
    # M = integer_uniform(1, 7)
    # positions of zeros and singularities of the reducible part
    # zeros_and_sings = [random.uniform(0, 1) for i in range(M)]
    zeros_and_sings = [sp.Rational(random.uniform(0, 1)) for i in range(M)]

    # multiplicity of each zero/singularity
    multiplicities = [discrete_distribution(
        [-2, -1, 0, 1, 2], [1/8, 1/8, 1/2, 1/8, 1/8]) for i in range(M)]
    # vertical scaling/horizontal asymptote if applicable
    # h = np.random.normal(0, 5)
    h = sp.Rational(np.random.normal(0, 5))

    # conclude numerator and denominator
    numerator = 1
    denominator = 1
    for i in range(M):
        if (multiplicities[i] > 0):
            numerator *= (x - zeros_and_sings[i]) ** multiplicities[i]
        elif (multiplicities[i] < 0):
            denominator *= (x - zeros_and_sings[i]) ** (-multiplicities[i])

    return numerator, denominator


def get_irreducible():
    # degree of numerator and denominator, respectively, of irreducible part
    m = integer_uniform(0, 4)
    n = integer_uniform(0, 4)
    # m = integer_uniform(0, 5)
    # n = integer_uniform(0, 5)
    # coefficients for non-leading terms of numerator and denomoinator of irreducible part
    # c = [random.uniform(-5, 5) for i in range(m)]
    # d = [random.uniform(-5, 5) for i in range(n)]
    c = [sp.Rational(random.uniform(-5, 5)) for i in range(m)]
    d = [sp.Rational(random.uniform(-5, 5)) for i in range(n)]
    numerator = x ** m
    for i in range(m):
        numerator += c[i] * x ** i
    denominator = x ** n
    for i in range(n):
        denominator += d[i] * x ** i

    return numerator, denominator


def get_random_rational_function():

    irred_numerator, irred_denominator = get_irreducible()
    red_numerator, red_denominator = get_reducible()

    return red_numerator * irred_numerator, red_denominator * irred_denominator
