'''
Created on 26 feb. 2022

!!!! PERTURBATION MODULE WAS MODIFIED!!! ---> Adapt

@author: ceci
'''
import sys
sys.path.append('../')
from Models.Propagation import Propagator
from Models.Perturbations import central_body
from Models.plots import plot_orbits
from Models.orbitData import Period
import numpy as np

# Initial State Vector
sat_SV1=np.array([6628.0, 0.0, 0.0, 0.0, 7.75, 0.0])
print(sat_SV1)
"""
--------------------------------------------------------------------
Propagate one inner orbit
--------------------------------------------------------------------
"""
rp=np.sqrt(sat_SV1[0]*sat_SV1[0]+sat_SV1[1]*sat_SV1[1]+sat_SV1[2]*sat_SV1[2]) # Radius of inner circular orbit
o1_period=Period(rp)
dt1=int(round(o1_period))
p = Propagator(stateVector=sat_SV1, step=100) 
p.RK4(dt1,[central_body]) 
sat_SV1=p.get_svs()[-1] # New initial State Vector
print(sat_SV1)

"""
Computes Hohmann transfer orbit's semimajor-axis and Delta V 
--------------------------------------------------
dV_p: delta V in perigee
dV_a: delta V in apogee
Vh_p: Hohmann transfer orbit velocity in perigee
Vh_a: Hohmann transfer orbit velocity in perigee
Vp: Velocity in perigee (inner circular orbit)
Va: Velocity in apogee (outer circular orbit)
--------------------------------------------------
"""
mu = 398600.448

ra=42164.0 # r position of Hohmann transfer orbit at apogee
"""First Delta V at perigee"""
Vp=np.sqrt(sat_SV1[3]*sat_SV1[3]+sat_SV1[4]*sat_SV1[4]+sat_SV1[5]*sat_SV1[5])
a_h=(rp+ra)/2 # Hohmann transfer orbit's semimajor-axis
Vh_p=np.sqrt(mu*((2/rp)-(1/a_h)))
dV_p=Vh_p-Vp

"""
--------------------------------------------------------------------
Add Delta V1 to State Vector and propagate half orbit
--------------------------------------------------------------------
"""
sat_SV1[4]=sat_SV1[4]+dV_p
ht_period=Period(a_h)
dt2=int(round(ht_period/2))
p_h = Propagator(stateVector=sat_SV1, step=100) 
p_h.RK4(dt2,[central_body])
sat_SV1=p_h.get_svs()[-1] # New initial State Vector
print(sat_SV1)

"""Second Delta V at apogee"""
Vh_a=np.sqrt(sat_SV1[3]*sat_SV1[3]+sat_SV1[4]*sat_SV1[4]+sat_SV1[5]*sat_SV1[5])
Va=np.sqrt(mu/ra)
dV_a=Va-Vh_a
sat_SV1[4]=sat_SV1[4]-dV_a
o2_period=Period(ra)
dt3=int(round(o2_period))
p_g = Propagator(stateVector=sat_SV1, step=100) 
p_g.RK4(dt3,[central_body])


plot_orbits([p.get_svs(),p_h.get_svs(),p_g.get_svs()])

print('Fin propagacion')
    