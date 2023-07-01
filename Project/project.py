#!/usr/bin/env python
# coding: utf-8

# In[68]:


import random
from decimal import Decimal
import math
from itertools import combinations
from typing import Callable
from math import sqrt
import numpy as np
import time

start_time = time.time()


def lj_potential(x: float) -> float:  # obfuscated, but fast implementation!
    r6 = 1 / x / x
    r6 *= r6 * r6
    return 4 * r6 * (r6 - 1)


def lj_potential_cut(x: float) -> float:
    if x >= 2.5:
        return 0
    else:
        return lj_potential(x)-lj_potential(2.5)


def pairwise_potential(potential: Callable[[float], float], xss: [[float]], box: float) -> float:
    """
    >>> lj13 = [
    ...     [  1.0132226417,  0.3329955686,  0.1812866397],
    ...     [   0.7255989775, -0.7660449415,  0.2388625373],
    ...     [   0.7293356067, -0.2309436666, -0.7649239428],
    ...     [   0.3513618941,  0.8291166557, -0.5995702064],
    ...     [   0.3453146118, -0.0366957540,  1.0245903005],
    ...     [   0.1140240770,  0.9491685999,  0.5064104273],
    ...     [  -1.0132240213, -0.3329960305, -0.1812867552],
    ...     [  -0.1140234764, -0.9491689127, -0.5064103454],
    ...     [  -0.3513615244, -0.8291170821,  0.5995701458],
    ...     [  -0.3453152548,  0.0366956843, -1.0245902691],
    ...     [  -0.7255983925,  0.7660457628, -0.2388624662],
    ...     [  -0.7293359733,  0.2309438428,  0.7649237858],
    ...     [   0.0000008339,  0.0000002733,  0.0000001488],
    ... ]
    >>> pairwise_potential(lj_potential, lj13)
    -44.326801418734654
    """

    Sum = 0

    # box accounts for periodic boundary condition
    for xi, xj in combinations(xss, 2):
        d = 0
        for k in range(len(xi)):
            if xi[k]-xj[k] < -box/2:
                d += (xi[k]+box-xj[k])**2
            elif xi[k]-xj[k] > box/2:
                d += (xi[k]-box-xj[k])**2
            else:
                d += (xi[k]-xj[k])**2
        Sum += potential(d**0.5)

    return Sum


def phi_A(r: float) -> float:
    alpha = 1
    rc = 2.0
    r2 = 1/r**2
    if r >= rc:
        return 0
    else:
        return alpha*(r2-1)*(rc**2*r2-1)**2


# In[ ]:


def phi_C(r: float) -> float:
    alpha = 114
    rc = 1.2
    r2 = 1/r**2
    if r >= rc:
        return 0
    else:
        return alpha*(r2-1)*(rc**2*r2-1)**2


# In[194]:


def init_mc(rho: float, L: float, type: int) -> np.ndarray:
    if type not in (0, 1):
        raise ValueError(
            "Invalid value for 'type' parameter. It must be 0 or 1. 0 for random positions, 1 for ordered lattice")

    N = int(rho * L**2)
    n = int(np.sqrt(N))

    if type == 1:
        coordinates = np.zeros((n**2, 2))

        s = L / n
        shift = (L-(n-1)*s)/2

        k = 0
        for i in range(n):
            for j in range(n):
                coordinates[k] = [i * s+shift, j * s+shift]
                k += 1

        return coordinates

    if type == 0:
        coordinates = np.zeros((N, 2))
        count = 0
        while count < N:
            x = np.random.uniform(0, L)
            y = np.random.uniform(0, L)
            if count == 0:
                coordinates[count] = [x, y]
                count += 1
            else:
                distances = np.linalg.norm(
                    coordinates[:count] - np.array([x, y]), axis=1)
                if np.all(distances >= 0.5):
                    # print(distances)
                    coordinates[count] = [x, y]
                    count += 1

        return coordinates


T1 = 0.728
rho1 = 0.8442

init_config = init_mc(rho1, 10, 0)
# print(init_config)
print("total atomic potential energy is:",
      pairwise_potential(phi_A, init_config, 10))
print("total colloidal potential energy is:",
      pairwise_potential(phi_C, init_config, 10))
print("total LJ potential energy is:", pairwise_potential(
    lj_potential_cut, init_config, 10))


# In[152]:


a = -np.sqrt(2)
b = 0.0134

a = Decimal(a)
b = Decimal(b)

remainder = a % b


def my_remainder(a: float, b: float):
    dec_b = Decimal(str(b))
    remainder = Decimal(str(a)) % Decimal(str(b))
    if remainder < 0:
        return float(remainder+dec_b)
    return float(remainder)


# In[199]:


def mc_simulation(total_step: float, T: float, box: float, sigma: float, coordinates: np.ndarray):
    # T is the temparature; sigma is the magnitude of random displacement
    N = coordinates.shape[0]
    energies = list(range(total_step))

    for i in range(total_step):
        e_old = pairwise_potential(phi_A, coordinates, box)
        rand_index = np.random.randint(0, N)
        displace_x = np.random.normal(0, sigma)
        displace_y = np.random.normal(0, sigma)
        coordinates[rand_index][0] = my_remainder(
            (coordinates[rand_index][0]+displace_x), box)
        coordinates[rand_index][1] = my_remainder(
            (coordinates[rand_index][1]+displace_y), box)
        e_new = pairwise_potential(phi_A, coordinates, box)

        random_number = random.random()
        if random_number < np.exp(-(e_new-e_old)/T):

            energies[i] = e_new
        else:
            energies[i] = e_old
            coordinates[rand_index][0] = my_remainder(
                (coordinates[rand_index][0]-displace_x), box)
            coordinates[rand_index][1] = my_remainder(
                (coordinates[rand_index][1]-displace_y), box)
        np.save('final_config_mc.npy', coordinates)

    return energies


energies = mc_simulation(50000, T1, 10, 2, init_config)

print(energies)
end_time = time.time()
print(f"It took {end_time-start_time:.2f} seconds to compute")
