'''
Created on 26 sep. 2021

@author: ceci
'''
from Models.Propagation import Propagator
from Models.Perturbations import central_body, j2
from Models.plots import plot_orbits
import numpy as np



if __name__ == '__main__':
    
    """
    Comentario de prueba
    1- Instancia un satelite -- hacer clase (masa) --> method getOrbit()
    2- Instancia una orbita
    3- Propagador
    """
    
    sat_SV=np.array([42164.0, 0.0, 0.0, 0.0, 3.07, 0.0])
    sat_SV1=np.array([7164.0, 0.0, 0.0, 0.0, 7.5, 0.0])

    
    p = Propagator(stateVector=sat_SV, step=100) 
    p.RK4(44000,[central_body])   
    
    p1 = Propagator(stateVector=sat_SV1, step=100) 
    p1.RK4(180000,[central_body, j2]) 
    
    for sv in p1.get_svs():
        print (sv)
        
    plot_orbits([p1.get_svs()])
    
    print('Fin propagacion')
    
