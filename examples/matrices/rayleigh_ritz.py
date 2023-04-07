import numpy as np
from numpy import ndarray
from numpy.linalg import norm

from local_optimisation.bfgs import bfgs


def rayleigh_ritz(
        aa: ndarray,
        eigenvector0: ndarray,
        tol: float = 1e-6) -> (float, ndarray):
    """
    Find the smallest (most negative) eigenvalue and associated unit eigenvector of matrix aa,
    to a tolerance in the value and gradient of the Rayleigh--Ritz function equal to tol.

    Uses BFGS for the minimisation.
    """

    def ralyeigh_ritz_function(eigenvector: ndarray) -> float:
        v = eigenvector[:, np.newaxis]
        return ((v.T @ aa @ v) / (v.T @ v))[0, 0]

    def rayleigh_ritz_gradient(eigenvector: ndarray) -> ndarray:
        v, v_t = eigenvector[:, np.newaxis], eigenvector[np.newaxis, :]
        gradient = 2 * ((v.T @ v) * (aa @ v) - v @ (v.T @ aa @ v)) / (v.T @ v) ** 2
        return gradient.flatten()

    xmin = bfgs(ralyeigh_ritz_function, rayleigh_ritz_gradient, eigenvector0, tol, tol)
    return ralyeigh_ritz_function(xmin), xmin / norm(xmin)
