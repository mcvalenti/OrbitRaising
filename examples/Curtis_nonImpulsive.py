'''
Created on 25 ago. 2022

@author: ceci
'''
from Models.Propagation1 import Propagator, xv2eo, r_v_Dtheta
from Models.Perturbations import central_body, thrust_force
from Models.plots import orbit, plot_orbits
from Models.orbitData import semimajorAxis, Period
import numpy as np



if __name__ == '__main__':
    
    """
    Curtis- Chapter 6 - non impulsive example
    """
    thrust0=10000.0
    rt=6378 # Earth radius
    rp=480 # Perigee radius
    ra=800 # Apogee radius
    sat_SV=np.array([6858,0,0,0,7.7102,0,2000])
    #--------------------
    # Orbit 1 - Initial
    #-------------------
    p_init = Propagator(stateVector=sat_SV, step=1, mass=2000, thrust=thrust0, isp=300) 
    a1=semimajorAxis(rp, ra)
    period1=Period(a1)
    #p_init.RK4(period1,[central_body])
    p_init.RK4_matrix(period1,[central_body])
    
    # -----------------------------------------------------
    # Transfer Orbit
    # Computes t_burn (time of propulsion) to reach apogee
    # Result t=261.1127 [s]
    # -----------------------------------------------------
    p = Propagator(stateVector=sat_SV, step=0.1, mass=2000, thrust=thrust0, isp=300) 
    t_burn0=100 # [s]
    tol=10000 # tolerance with final solution
    r_a=22378.0 # Desired apogee [km]
    #p.RK4(t_burn0,[central_body, thrust_force]) 
    p.RK4_matrix(t_burn0,[central_body, thrust_force]) 
    print('Computing Transfer orbit propulsing ... wait')
    while (tol>100): # tolerance with final solution [km]
        # Propagate until t_burn0
        #p.RK4(t_burn0,[central_body, thrust_force]) 
        p.RK4_matrix(t_burn0,[central_body, thrust_force]) 
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
        print( t_burn0,ra, r_a-ra,last_sv[-1])
        t_burn0=t_burn0+1 # meaning 1 sec
    print('Transfer orbit completed')
    print('t_burn:',t_burn0)
    print('ra:',ra)
    
    # --------------------
    # Orbit 2 - to Apogee
    # --------------------
    
    period2=Period(a)
    p1 = Propagator(stateVector=p.last_sv(), step=1, mass=p.last_sv()[6], thrust=thrust0, isp=300)
    #p1.RK4(period2/2,[central_body]) 
    p1.RK4_matrix(period2/2,[central_body]) 
    
    # ------------------------------------
    # Propulsing time for Circularization
    # ------------------------------------
    print('Computing Circularization ... wait')
    tol1=1000
    t_burn1=1
    pc = Propagator(stateVector=p1.last_sv(), step=1, mass=p1.last_sv()[6], thrust=thrust0, isp=300) 
    while (tol1>100):
        # Propagate until a=ra
        pc.RK4(t_burn1,[central_body, thrust_force]) 
        last_sv=pc.last_sv()
        r_current = np.array([last_sv[0],last_sv[1],last_sv[2]])
        v_current = np.array([last_sv[3],last_sv[4],last_sv[5]])
        # Compute true anomaly
        a,e,i,Omega,w,nu=xv2eo(r_current,v_current)
        tol1=np.abs(ra-a)
        t_burn1=t_burn1+1 # meaning 1 sec

    # ------------------------------------
    # Circularized orbit
    # ------------------------------------
    period3=Period(a)
    pf = Propagator(stateVector=pc.last_sv(), step=1, mass=pc.last_sv()[6], thrust=thrust0, isp=300) 
    pf.RK4(period3-1600,[central_body])
    
    
    print ('End of processing')
    plot_orbits([p_init.get_svs(),p.get_svs(),p1.get_svs(),pc.get_svs(),pf.get_svs()])
    