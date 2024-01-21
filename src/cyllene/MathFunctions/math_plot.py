import matplotlib.pyplot as plt
import sympy as sp

from .math_rfunction import RFunction


def determine_xrange(func: RFunction):


    relevant_pts = sp.EmptySet

    # add boundary of domain as relevant (if implemented)
    try:
        relevant_pts += func.domain.boundary
    except NotImplementedError:
        # this is the case for trig functions, for example
        # do nothing
        pass

    # add zeros
    relevant_pts += func.zeros

    # add critical points
    relevant_pts += func.critical_points

    # add potential inflection points
    relevant_pts += func.inflection_points

    if relevant_pts == sp.EmptySet:
        # no relevant points -> return generic interval
        return -6,6

    if not isinstance(relevant_pts, sp.sets.sets.FiniteSet):
        # infinitely many relevant pts
        # try intersection with compact interval
        relevant_pts = sp.Intersection(relevant_pts, sp.Interval(-6,6))
        if not isinstance(relevant_pts, sp.sets.sets.FiniteSet):
            # if this does not yield a finite set, resort to generic
            return -6,6
 
    delta = relevant_pts.sup - relevant_pts.inf
    return relevant_pts.inf - delta, relevant_pts.sup + delta
