from typing import Callable

from numpy import ndarray
from numpy.linalg import norm

from .line_search import line_search


def gradient_descent(
        f: Callable[[ndarray], float],
        df: Callable[[ndarray], ndarray],
        x0: ndarray,
        tol: float) -> ndarray:
    """
    Using the steepest descent method, find a minimum of a function f with first derivative g
    in the region of the point x0.
    """

    def gradient_descent_step():
        df0 = df(x0)
        p = -df0 / norm(df0)
        alpha = line_search(f, x0, p, df0)
        return x0 + alpha * p

    while norm((x1 := gradient_descent_step()) - x0) > tol:
        x0 = x1

    return x1
