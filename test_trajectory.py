'''
Created on 13 dic. 2022

@author: ceci
'''
import numpy as np
from Models.Propagation1 import xv2eo

def C2quat(C):
    """
    input DCM matrix 3x3 
    """
    # 1st Step - search maximum
    b0_2=(1/4.0)*(1+np.trace(C))
    b1_2=(1/4.0)*(1+2*C[0,0]-np.trace(C))
    b2_2=(1/4.0)*(1+2*C[1,1]-np.trace(C))
    b3_2=(1/4.0)*(1+2*C[2,2]-np.trace(C))
    beta_squares=np.array([b0_2,b1_2,b2_2,b3_2])
    # 2nd Step - Equations for the rest of the parameters
    b0b1=(C[1,2]-C[2,1])/4.0
    b0b2=(C[2,0]-C[0,2])/4.0
    b0b3=(C[0,1]-C[1,0])/4.0
    b1b2=(C[0,1]+C[1,0])/4.0
    b3b1=(C[2,0]+C[0,2])/4.0
    b2b3=(C[1,2]+C[2,1])/4.0
    if np.argmax(beta_squares)==0:
        b1=b0b1/np.sqrt(b0_2)
        b2=b0b2/np.sqrt(b0_2)
        b3=b0b3/np.sqrt(b0_2)
        quat_vect=np.array([np.sqrt(b0_2),b1,b2,b3])
    if np.argmax(beta_squares)==1:
        b0=b0b1/np.sqrt(b1_2)
        b2=b1b2/np.sqrt(b1_2)
        b3=b3b1/np.sqrt(b1_2)
        quat_vect=np.array([b0,np.sqrt(b1_2),b2,b3])
    if np.argmax(beta_squares)==2:
        b0=b0b2/np.sqrt(b2_2)
        b1=b1b2/np.sqrt(b2_2)
        b3=b2b3/np.sqrt(b2_2)
        quat_vect=np.array([b0,b1,np.sqrt(b2_2),b3])
    if np.argmax(beta_squares)==3:
        b0=b0b3/np.sqrt(b3_2)
        b1=b3b1/np.sqrt(b3_2)
        b2= b2b3/np.sqrt(b3_2)
        quat_vect=np.array([b0,b1,b2,np.sqrt(b3_2)])
    return quat_vect

def trajectory(y0,a,t,dt,int0):
    int0=0
    return {}

def test_trajectory1(x0,v0):
    # xt matrix will hold n x 16 elements. Each column is: time [s]
    # position and velocity [cartesian, km and km/s], keplerian elements and
    # maneuver acceleration ]km, three axis, cartesian]
    
    wet_mass=200 # [km]
    # Apollo ACE
    isp=1400 # [s]
    thrust = 0.05 # [N]
    
    flow_rate =thrust /(isp*9.81) #[kg/s]
    duration = 38640000
    #Initial COnditions
    y0=[]
    y0[0:3]=x0
    y0[3:6]=v0
    y=y0
    dt=100 # each step is 100s
    i=0
    i2=0
    n = duration/dt 
    maneuver_type =1
    t = 0
    tnode = 0
    tsample = 10000
    nnode = 0
    nsample = 4
    a = 0 
    ex = np.zeros(12,dtype=float)
    ax = np.zeros(6, dtype=float)
    quat=[0,0,0,0]
    xt=[]
    while t < duration:
        ma = thrust/wet_mass/1000 # [km/s2]
        versor_v = y0[3:6]/np.linalg.norm(y0[4:6]) # velocity versor
        
        if maneuver_type==1:
            if (i>(nnode + nsample)) or (i==1):
                nnode = i
                a = ma*versor_v
                ex[i2,0]=t
                ex[i2,1:7]=y
                ex[i2,7]=1000
                ex[i2,8:11]=a/np.linalg.norm(a)
                # Compute the rotation quaternion to build the 
                # export attitude file
                versor_p=y0[0:3]/np.linalg.norm(y0[0:3])
                versor_n=np.cross(versor_p,versor_v)
                versor_n=np.linalg.norm(versor_n)
                # Rotation Matrix
                rm=np.array([versor_v,
                             versor_n,
                             np.cross(versor_v,versor_n)])
                quat=C2quat(np.transpose(rm))
                ax[i2,0]=t
                ax[i2,1:5]=quat
                i2=i2+1
        elif maneuver_type==2:
            if (i>(nnode + nsample)) or (i==1):
                nnode= i 
                a = ma* [0,1,0]
                ex[i2,0]=t
                ex[i2,1:7]=y
                ex[i2,7]=1000
                ex[i2,8:11]=a/np.linalg.norm(a)
                # Rotation Matrix
                rm=np.array([[0,1,0],
                             [0,0,-1],
                             [-1,0,0]])
                quat=C2quat(np.transpose(rm))
                ax[i2,0]=t
                ax[i2,1:5]=quat
                i2=i2+1
                
    [y,dt] = trajectory(y0,a,t,dt,0)
    kep = xv2eo(y[0:3], y[3:6])# return a,e,i,Omega,w,nu
    
    if (kep[2] > 42000) and (maneuver_type==1): # Semimajor axis reached target, switch to inertial maneuver
        maneuver_type=2
    elif (kep[2]<0.02) and (maneuver_type==2):
        maneuver_type=99
        
    xt[i,0]=t 
    xt[i,1:7]=y 
    xt[i,7:13]=kep 
    xt[i,13:16]= a 
    xt[i,17]= maneuver_type
    
    return xt, ex, ax