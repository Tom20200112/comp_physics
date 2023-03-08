import numpy as np

def morse_potential(x: float, rho: float, epsilon: float = 1.0, r0: float = 1.0) -> float:
    exp=np.exp(rho*(1-x/r0))
    return epsilon*exp*(exp-2)