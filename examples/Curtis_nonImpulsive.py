'''
Created on 25 ago. 2022

@author: ceci
'''
from Models.Propagation1 import Propagator, xv2eo, r_v_Dtheta
from Models.Perturbations import central_body, thrust_force
from Models.plots import orbit, plot_orbits
import numpy as np



if __name__ == '__main__':
    
    """
    Curtis- Chapter 6 - non impulsive example
    """
    rt=6378 # Earth radius
    rp=480 # Perigee radius
    ra=800 # Apogee radius
    sat_SV=np.array([6858,0,0,0,7.7102,0,2000])
    #--------------------
    # Orbit 1 - Initial
    #-------------------
    p_init = Propagator(stateVector=sat_SV, step=1, mass=2000, thrust=1000, isp=300) 
    p_init.RK4(5400,[central_body])
    
    # -----------------
    # Transfer Orbit
    # -----------------
    p = Propagator(stateVector=sat_SV, step=0.1, mass=2000, thrust=10000, isp=300) 
    # tiempo resultado t=261.1127 [s] 
    t_burn0=1
    t_burn_step=t_burn0*10
    tol=10000 # final solution 22378 km
    r_a=22378.0
    #r_a=10270.0
    count=0
    p.RK4(t_burn0,[central_body, thrust_force]) 
 
    while (tol>10 or t_burn0 > 500):
        # Propagate until t_burn0
        count=count+1
        p.RK4(t_burn0,[central_body, thrust_force]) 
        last_sv=p.last_sv()
        r_current = np.array([last_sv[0],last_sv[1],last_sv[2]])
        v_current = np.array([last_sv[3],last_sv[4],last_sv[5]])
        # Compute true anomaly
        a,e,i,Omega,w,nu=xv2eo(r_current,v_current)
        d_nu=np.pi-nu
        # Compute r apogee
        ra,va=r_v_Dtheta(r_current,v_current,d_nu)
        ra=np.linalg.norm(ra)
        tol=np.abs(r_a-ra)
        #print( t_burn0,ra, r_a-ra,last_sv[-1])
        t_burn0=t_burn0+0.1 # meaning 1 sec
        
    
    
    # p1 = Propagator(stateVector=p.last_sv(), step=1, mass=p.last_sv()[6], thrust=10000, isp=300)
    # p1.RK4(12000,[central_body]) 
    print ('End of processing') 
    
    #plot_orbits([p_init.get_svs(),p.get_svs(),p1.get_svs()])
                 
                 