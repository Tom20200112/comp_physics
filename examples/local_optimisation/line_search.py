from typing import Callable

from numpy import ndarray


def line_search(
        f: Callable[[ndarray], float],
        x: ndarray,
        p: ndarray,
        gx: ndarray,
        c: float = 0.5,
        t: float = 0.5,
        max_alpha: float = 1.0) -> float:
    """
    Perform a backtracking line search based on the Armijo–Goldstein condition
    c scales the threshold above which the step is rejected,
    t scales the step upon rejection
    """
    m = p @ gx
    if m >= 0:
        raise ValueError(f"no function decrease guaranteed in search direction p (p @ gx = {p @ gx})")

    fx = f(x)
    alpha = max_alpha

    while f(x + alpha * p) > fx + c * alpha * m:
        alpha *= t

    return alpha
