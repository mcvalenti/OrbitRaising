'''
Created on 26 sep. 2021

@author: ceci
'''
import numpy as np

def central_body(**kwargs):
    """ 
    Computes gravity accelerations of central body force
    input: stateVector [array]
    output: acceleration vector for each components [km2/s]
    """
    stateVector=kwargs['statevector']
    mu=398600.448 # km3/s2
    r_vect=np.array([stateVector[0],stateVector[1],stateVector[2]])
    r = np.linalg.norm(r_vect)
    coeff = -(mu)/(r**3)
    return np.array([stateVector[0]*coeff,stateVector[1]*coeff,stateVector[2]*coeff,0])

def j2(**kwargs):
    """
    Computes J2 Earth Gravity potential term perturbations
    output: acceleration vector for each components [km2/s]
    """
    stateVector=kwargs['statevector']
    mu=398600.448 # km3/s2
    j2=1.0826157e-3
    Re= 6378.135 #[km]
    r_vect=np.array([stateVector[0],stateVector[1],stateVector[2]])
    r = np.linalg.norm(r_vect)
    cte_c=j2*mu*Re/2
    
    acc_x=3*cte_c*(1/r**5)*(1-(5*stateVector[2]**2)/r*r)
    acc_y=3*cte_c*(1/r**5)*(1-(5*stateVector[2]**2)/r*r)
    acc_z=3*cte_c*(1/r**5)*(3-(5*stateVector[2]**2)/r*r)
    
    return np.array([acc_x,acc_y,acc_z,0])

def thrust_force(**kwargs):
    """ 
    Computes thrust forces and mass consumption
    input: stateVector_mass [array, dim:7] - The state vector considers
            the satellite mass
    output : acceleration vector for each components [km2/s] and
            mass consumption
    """
    stateVector=kwargs['statevector']
    thrust=kwargs['thrust']
    isp=kwargs['isp']
    g0=9.81 # [km/s2]
    v_vect=np.array([stateVector[3],stateVector[4],stateVector[5]])
    v_mod=np.linalg.norm(v_vect)
    coeff=thrust/(stateVector[6]*v_mod*1000) # Thrust aligned with velocities [km/s2]
    return np.array([stateVector[3]*coeff,stateVector[4]*coeff,stateVector[5]*coeff,-thrust/(isp*g0)])
