import sys
import os

sys.path.append("/Users/tomzhang/Documents/计算物理/examples")

from typing import Callable

import numpy as np
from numpy import ndarray
from numpy.linalg import norm

from matrices import rayleigh_ritz
from .bfgs import bfgs_update_hessian
from .line_search import line_search


def get_hessian_approximator(
        df: Callable[[ndarray], ndarray],
        h: float = 1e-4):
    """
    Returns a function that approximates the Hessian of the function with gradient df.
    """

    def central_differences(x: ndarray) -> ndarray:
        """
        Central differences approximation to the Hessian of the function with derivative df, at x
        """
        n = x.size
        hessian = np.zeros((n, n), dtype=float)
        for i in range(n):
            x[i] += h
            hessian[i, :] += df(x)
            x[i] -= 2 * h
            hessian[i, :] -= df(x)
            x[i] += h
        return hessian / 2 / h

    return central_differences


def project_out(
        aa: ndarray,
        v: ndarray) -> ndarray:
    """
    Project the vector v out of the matrix aa.
    """
    return aa - (aa @ v) * v


def hybrid_eigenvector_following(
        f: Callable[[ndarray], float],
        df: Callable[[ndarray], ndarray],
        x0: ndarray,
        d2f: Callable[[ndarray], ndarray] | None = None,
        tolg: float = 1e-5,
        tolev: float = 1e-6) -> ndarray:
    """
    Apply hydrid eigenvector following / BFGS to the function f at point x0,
    attempting to converge to a first-order saddle of f.

    If the function to compute the Hessian, d2f, is not given, the Hessian
    is approximated using central differences.

    Continue until the magnitude of the gradient is less than tolg.
    At each step, the smallest eigenvalue is converged to a tolerance tolev.
    """
    x0 = x0.copy()
    binv = np.eye(x0.size)
    dfx0 = df(x0)
    modg = norm(dfx0)
    evec0 = np.random.randn(x0.size)

    if d2f is None:
        d2f = get_hessian_approximator(df)

    def negativef(x_):
        return -f(x_)

    while modg > tolg:
        # Eigenvector part
        d2f0 = d2f(x0)
        eval_, evec = rayleigh_ritz(d2f0, evec0, tolev)

        if eval_ >= 0.0:
            raise ValueError("smallest eigenvalue is positive; aborting search")

        if f(x0 - 1e-12 * evec) > f(x0 + 1e-12 * evec):
            evec *= -1.0
        evec0[:] = evec

        gx_ = -(dfx0 @ evec) * evec

        if evec @ gx_ < 0:
            alpha = line_search(negativef, x0, evec, gx_, max_alpha=0.1)
            x0 = x0 + alpha * evec

        # BFGS part
        p = -binv @ dfx0
        dfx0 = project_out(dfx0, evec)
        p = project_out(p, evec)
        p /= norm(p)

        alpha = line_search(f, x0, p, dfx0, max_alpha=0.1)
        x0 = x0 + alpha * p
        s = alpha * p
        gx_new = df(x0)
        binv = bfgs_update_hessian(binv, gx_new - dfx0, s)
        dfx0 = gx_new
        modg = norm(dfx0)

    return x0
