import cython

DTYPE = float

import itertools
from typing import Callable
from itertools import combinations
from typing import Callable
from math import sqrt
import numpy as np
from math import dist
from functools import partial
from time import time as time
import random

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def sph_cartesian(angle: [float]):
    coordinate=[]
    coordinate.append(np.sin(angle[0])*np.cos(angle[1]))
    coordinate.append(np.sin(angle[0])*np.sin(angle[1]))
    coordinate.append(np.cos(angle[0]))
    
    return coordinate


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)   
def coulomb_potential(r: float)->float:
    return 1/r

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def pairwise_coulomb_potential_c(angles: [[float]]):
    cdef Py_ssize_t i,j,k
    cdef int particles=angles.size//2
    cdef double r2
    cdef double energy=0.0

    positions=np.array([sph_cartesian(xi) for xi in angles])

    for i in range(particles):
        for j in range(i+1,particles):
            r2=0.0
            for k in range(3):
                r2+=(positions[i][k]-positions[j][k])*(positions[i][k]-positions[j][k])
            energy+=coulomb_potential(np.sqrt(r2))

    return energy


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def pairwise_coulomb_potential_gradient_c(angles:[[float]]):
    cdef Py_ssize_t i,j
    cdef float sum
    cdef int n

    #angles_array=np.array(angles)
    n=len(angles)
    # angles_flat=angles_array.flatten()
    gradient_components=np.zeros_like(angles)
    positions=np.array([sph_cartesian(xi) for xi in angles])
    
    for i in range(n):
        # calculate partial theta first
        theta_i=angles[i][0]
        phi_i=angles[i][1]
        coordinate_i=positions[i]
        sum=0
        for j in range(n):
            if j!=i:
                coordinate_j=positions[j]
                distance=dist(coordinate_i,coordinate_j)
                sum+=(2*(coordinate_i[0]-coordinate_j[0])*(np.cos(theta_i))*(np.cos(phi_i))+2*(coordinate_i[1]-coordinate_j[1])*(np.cos(theta_i))*(np.sin(phi_i))+2*(coordinate_i[2]-coordinate_j[2])*(0-np.sin(theta_i)))*(0-1/distance**3)/2
        gradient_components[i][0]=sum
        
        # calculate partial phi next
        sum=0
        for j in range(n):
            if j!=i:
                coordinate_j=positions[j]
                distance=dist(coordinate_i,coordinate_j)
                sum+=((coordinate_i[0]-coordinate_j[0])*(0-np.sin(theta_i))*(np.sin(phi_i))+(coordinate_i[1]-coordinate_j[1])*(np.sin(theta_i))*(np.cos(phi_i)))*(0-1/distance**3)
        gradient_components[i][1]=sum
    
    return gradient_components.reshape((-1,2))
