import numpy as np
import matplotlib.pyplot as plt

def regular_polygon(i:int) -> float:
    # Enter an integer i to calculate the perimeter of 2^i-sided regular polygon inscribing the circle
    n=1
    l=2
    while n<i:
        l=2**(n+1)*np.sqrt(1/2-np.sqrt(1/4-(l/2**(n+1))**2))
        n+=1
    
    return l

def estimate_pi_in(sides:[int])->float:
    # return an estimated pi_infinity using the given 2^i-sided inscribed polygons in the list
    pi=np.array([regular_polygon(j) for j in sides])
    pi=pi.reshape(len(sides),1)
    
    M=np.ones((len(sides),1))
    arr_sides=np.array(sides)
    for j in range(0,len(sides)-1):
        kj=np.float_power(2,-arr_sides*(j+1))
        kj=kj.reshape(len(sides),1)
        
        M=np.concatenate((M,kj),axis=1)
        
    return np.dot(np.linalg.inv(M),pi)[0,0]
        
t=[6,7,8,9]
pi=np.array([regular_polygon(j) for j in t])

fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(5,4))
ax.plot([1/te for te in t] , pi,marker='*',linestyle='')
plt.scatter(0, estimate_pi_in(t), marker='o')
plt.xlim(0,0.3)

plt.show()