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

import sys
import os

sys.path.append("/Users/tomzhang/Documents/计算物理/")

from examples import local_optimisation as lo
from examples import pair_potential as pp

chrome_number=int(input("The size of gene pool: "))
chrome_length=int(input("The length of each chromosome: "))
size=float(input("You want to constrain all particles in a cube with side length: "))
prob_of_mutation=float(input("You want the probability of mutating each gene to be: "))
num_of_generations=int(input("You want how many generations of evolution: "))

def encode(r: [float], m: int) -> [[int]]:
    code=[]
    for x in r:
        genes=[]
        for j in range(m):
            if j==0:
                genes.append(round(x))
            else:
                s=sum(genes[k]*2**(j-k-1) for k in range(j))
                genes.append(round(2**j*x-s))
        code.append(genes)
    
    return code
                
def decode(code: [[int]], m: int)-> [float]:
    r=[]
    for genes in code:
        s=0
        for j in range(m):
            s+=genes[j]/2**(j+1)
        r.append(s*size)
    return r
    
def init_population_lj38():
    chromes=[]
    
    for i in range(chrome_number):
        randoms=[]
        for j in range(38*3):
            randoms.append(np.random.random())
        chromes.append(encode(randoms,chrome_length))
        
    return chromes

def select(chromes: [[[float]]]):
    # hold tournaments for pairs of elements in "chromes", where the winners survive.
    survivers=[]
    #chromes=sort(chromes)
    
    if len(chromes)%2==0:
        for i in range(0,len(chromes),2):
            if pp.lj_energy_c(np.array(decode(chromes[i],chrome_length)))<pp.lj_energy_c(np.array(decode(chromes[i+1],chrome_length))):
                survivers.append(chromes[i])
            else:
                survivers.append(chromes[i+1])
    else:
        for i in range(0,len(chromes)-1,2):
            if pp.lj_energy_c(np.array(decode(chromes[i],chrome_length)))<pp.lj_energy_c(np.array(decode(chromes[i+1],chrome_length))):
                survivers.append(chromes[i])
            else:
                survivers.append(chromes[i+1])
        survivers.append(chromes[-1])
    
    """
    for i in range(len(chromes)//2):
        survivers.append(chromes[i])
    """
   
    return survivers

def cross(code1: [[int]],code2: [[int]]):
    child=[]
    for i in range(len(code1)):
        child_genes=[]
        for j in range(len(code1[i])//2):
            child_genes.append(code1[i][j])
        for j in range(len(code1[i])//2,len(code1[i])):
            child_genes.append(code2[i][j])
        child.append(child_genes)
    
    return child

def reproduce(survivers: [[[float]]]):
    new_generation=survivers.copy()
    for i in range(len(survivers),chrome_number):
        parents=random.sample(survivers,2)
        new_generation.append(cross(parents[0],parents[1]))
        
    return new_generation

def fitness(code: [[float]]):
    return pp.lj_energy_c(np.array(decode(code,chrome_length)))

def sort(chromes: [[[float]]]):
    for i in range(len(chromes)):
        for j in range(i+1,len(chromes)):
            if fitness(chromes[i])>fitness(chromes[j]):
                temp=chromes[i]
                chromes[i]=chromes[j]
                chromes[j]=temp
    
    return chromes

def mutate(chromes: [[[float]]]):
    chromes=sort(chromes)
    for i in range(len(chromes)//3,len(chromes)):
        for j in range(len(chromes[i])):
            for k in range(len(chromes[i][j])):
                r=np.random.random()
                if r<prob_of_mutation:
                    chromes[i][j][k]=1-chromes[i][j][k]

    return chromes

new_generation=init_population_lj38()


for i in range(num_of_generations):

    survivers=select(new_generation)
    new_generation=reproduce(survivers)
    new_generation=mutate(new_generation)

for j in range(len(new_generation)):
    print(fitness(new_generation[j]))
print(decode(new_generation[0],chrome_length))


"""
print(initial)
print(len(initial))
print(fitness(initial[0]))
print(fitness(initial[1]))
print(fitness(initial[2]))
print(select(initial))
print(mutate(select(initial)))
"""