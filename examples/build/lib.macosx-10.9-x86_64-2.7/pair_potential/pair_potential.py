import numpy as np


def pair_potential(x, potential=None, args=()):
    """

    Calculates the potential energy of configuration of n particles in d dimensions.

    :param x: positions of the particles
    :type x: numpy ndarray, shape n x d
    :param potential: the pairwise potential function.
                      must be of the form f(x, *args).
    :type potential: callable
    :param args: arguments to pass to the function

    :return: energy of the configuration
    :rtype: float
    """

    if potential is None:
        return 0.0

    n, _ = x.shape
    left, right = np.triu_indices(n, 1)
    r = np.linalg.norm(x[left] - x[right], axis=1)
    energy = np.sum(potential(r, *args))

    return energy
