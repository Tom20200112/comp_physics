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
def pairwise_coulomb_potential(angles: [[float]]):
    return sum(
        coulomb_potential(dist(sph_cartesian(xi),sph_cartesian(xj))) for xi,xj in combinations(angles,2)
    )

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def array_norm(v:np.array):
    v=np.array(v)
    square = np.sum(v * v)
    return np.sqrt(square)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def generate_cluster(N:int):
    col1=np.random.rand(N) * np.pi
    col2 = np.random.rand(N) * 2 * np.pi
    arr= np.column_stack((col1, col2))
    return arr


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def pairwise_coulomb_potential_gradient(angles:[[float]])->[[float]]:
    angles_array=np.array(angles)
    n,d=angles_array.shape
    angles_flat=angles_array.flatten()
    gradient_components=[]
    
    for i in range(n):
        # calculate partial theta first
        theta_i=angles[i][0]
        phi_i=angles[i][1]
        coordinate_i=sph_cartesian(angles[i])
        sum=0
        for j in range(n):
            if j!=i:
                coordinate_j=sph_cartesian(angles[j])
                distance=dist(coordinate_i,sph_cartesian(angles[j]))
                sum+=(2*(coordinate_i[0]-coordinate_j[0])*(np.cos(theta_i))*(np.cos(phi_i))+2*(coordinate_i[1]-coordinate_j[1])*(np.cos(theta_i))*(np.sin(phi_i))+2*(coordinate_i[2]-coordinate_j[2])*(0-np.sin(theta_i)))*(0-1/distance**3)/2
        gradient_components.append(sum)
        
        # calculate partial phi next
        sum=0
        for j in range(n):
            if j!=i:
                coordinate_j=sph_cartesian(angles[j])
                distance=dist(coordinate_i,sph_cartesian(angles[j]))
                sum+=((coordinate_i[0]-coordinate_j[0])*(0-np.sin(theta_i))*(np.sin(phi_i))+(coordinate_i[1]-coordinate_j[1])*(np.sin(theta_i))*(np.cos(phi_i)))*(0-1/distance**3)
        gradient_components.append(sum)
    
    return np.array(gradient_components).reshape((-1,d))

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def coulomb_gradient_descent(angles:[[float]],tol:float,c0:float=0.3,tau:float=0.5,max_alpha:float=1):
    
    c=np.array(angles)
    a=c
    b=a-pairwise_coulomb_potential_gradient(a)
    
    while array_norm(pairwise_coulomb_potential_gradient(b))>tol:
        gamma=abs(sum((a-b).flatten()*(pairwise_coulomb_potential_gradient(a)-pairwise_coulomb_potential_gradient(b)).flatten()))/(array_norm(pairwise_coulomb_potential_gradient(a)-pairwise_coulomb_potential_gradient(b)))**2
        c=b-gamma*pairwise_coulomb_potential_gradient(b)
        a=b 
        b=c
    
    return c
