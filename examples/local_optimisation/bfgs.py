from typing import Callable

import numpy as np
from numpy import ndarray
from numpy.linalg import norm

from .line_search import line_search


def bfgs_update_hessian(
        binv: ndarray,
        y: ndarray,
        s: ndarray) -> ndarray:
    """
    Update the approximate inverse Hessian matrix in the BFGS scheme
    using the Sherman-Morrison formula
    """
    y, y_t = y[:, np.newaxis], y[np.newaxis, :]
    s, s_t = s[:, np.newaxis], s[np.newaxis, :]
    if (s_t @ y) == 0:
        raise ValueError(f's_t @ y = {s_t} @ {y} = {s_t @ y}')
    elif (s_t @ y) < 0:
        y *= -1
    return (binv +
            (s_t @ y + y_t @ binv @ y) * (s @ s_t) / (s_t @ y) ** 2 -
            (binv @ y @ s_t + s @ y_t @ binv) / (s_t @ y))


def take_step(
        f: [[ndarray], float],
        x0: ndarray,
        df0: ndarray,
        binv: ndarray) -> ndarray:
    """
    Perform a line search and return an updated set of coordinates
    """
    p = -binv @ df0
    alpha = line_search(f, x0, p, df0)
    return x0 + alpha * p


def bfgs(
        f: Callable[[ndarray], float],
        df: Callable[[ndarray], ndarray],
        x0: ndarray,
        xtol: float,
        gtol: float) -> ndarray:
    """
    Using the Broyden-Fletcher-Goldfarb-Shanno method,
    find a minimum of a function f with first derivative g
    in the region of the point x0,
    to a coordinate tolerance xtol OR a gradient tolerance gtol.
    """

    x0 = x0.copy()
    df0 = df(x0)
    b_inv = np.eye(x0.size)
    while all((norm((x1 := take_step(f, x0, df0, b_inv)) - x0) > xtol, norm(df1 := df(x1)) > gtol), ):
        b_inv = bfgs_update_hessian(b_inv, df1 - df0, x1 - x0)
        x0, df0 = x1, df1
    return x1
