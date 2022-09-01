'''
Created on 26 sep. 2021

@author: ceci
'''
from Models.Propagation1 import Propagator
from Models.Perturbations import central_body, j2, thrust_force
from Models.plots import plot_orbits
import numpy as np



if __name__ == '__main__':
    
    """

    """
    perigee=480
    apogee=800
    sat_SV=np.array([42164.0, 0.0, 0.0, 0.0, 3.0, 0.0,1000])
    p = Propagator(stateVector=sat_SV, step=5, mass=2000, thrust=0.01, isp=300) 
    p.RK4(186000,[central_body, thrust_force])  
    # for sv in p.get_svs():
    #     print(sv)
    p.plot()
    
    print(p.get_svs()[0])
    print('Fin propagacion')
    
