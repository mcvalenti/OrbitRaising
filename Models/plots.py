'''
Created on 26 feb. 2022

@author: ceci
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def plot_orbits(stateVectors_list):
    
    ax=plt.axes() #(projection="3d")

    for svl in stateVectors_list:
        # ORBITS x, y, z coordinates
        x1 = []
        y1 = []
        z1 = []
    
        for e in svl:
            x1.append(e[0])
            y1.append(e[1])
            z1.append(e[2])
    
        ax.plot(x1, y1)
        
    plt.axis('equal')
    plt.show()
    
def orbit(stateVectors):
    """
    Plot just one orbit
    """
    ax=plt.axes(projection="3d")
    

    x1 = []
    y1 = []
    z1 = []
    for svl in stateVectors:
        x1.append(svl[0])
        y1.append(svl[1])
        z1.append(svl[2])
        
    ax.plot3D(x1, y1, z1, 'red')


    plt.show()
