'''
Created on 26 sep. 2021

@author: ceci
'''
import numpy as np

def central_body(stateVector):
    """ 
    Computes gravity acelerations of central body force
    input: stateVector [array]
    output: aceleration vector for each components [km2/s]
    """
    mu=398600.448 # km3/s2
    mod = np.linalg.norm(stateVector);
    coeff = -(mu)/(mod**3)
    return np.array([stateVector[0]*coeff,stateVector[1]*coeff,stateVector[2]*coeff])

def j2(stateVector):
    """
    Computes J2 Earth Gravity potential term perturbations
    output: aceleration vector for each components [km2/s]
    """
    
    mu=398600.448 # km3/s2
    j2=1.0826157e-3
    Re= 6378.135 #[km]
    mod = np.linalg.norm(stateVector);
    cte_c=j2*mu*Re/2
    
    acc_x=3*cte_c*(1/mod**5)*(1-(5*stateVector[2]**2)/mod*mod)
    acc_y=3*cte_c*(1/mod**5)*(1-(5*stateVector[2]**2)/mod*mod)
    acc_z=3*cte_c*(1/mod**5)*(3-(5*stateVector[2]**2)/mod*mod)
    
    return np.array([acc_x,acc_y,acc_z])
