'''
Created on 26 feb. 2022

@author: ceci
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def plot_orbits(stateVectors_list):
    
    fig=plt.figure(facecolor="Black")
    ax=plt.axes(projection="3d")
    
    u=np.linspace(0,2*np.pi,100)
    v=np.linspace(0,np.pi,100)
    r=6378
    
    
    # SPHERE x, y ,z coordinates
    x=r*np.outer(np.cos(u),np.sin(v))
    y=r*np.outer(np.sin(u),np.sin(v))
    z=r*np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot the surface.
    #surf = ax.plot_surface(x,y,z)
    
    for svl in stateVectors_list:
        # ORBITS x, y, z coordinates
        x1 = []
        y1 = []
        z1 = []
    
        for e in svl:
            x1.append(e[0])
            y1.append(e[1])
            z1.append(e[2])
    
        ax.plot3D(x1, y1, z1, 'red')
    
    # ax.set_xlim(-43000,10000)
    # ax.set_ylim(-43000,10000)
    # ax.set_zlim(-43000,10000)

    plt.show()
