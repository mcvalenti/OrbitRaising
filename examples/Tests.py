'''
Created on 26 sep. 2021

@author: ceci
'''

import numpy as np

# def deriv(t_inner,y_inner):
#     """
#     CURTIS - Example 1.17 - (pag 46)
#     """
#     acc_vect=np.array([y_inner[1],np.sin(0.4*t_inner)-y_inner[0]-2*(0.03)*y_inner[1]])
#     return acc_vect

def deriv(y_inner):
    """
    CURTIS - Example 1.20- (pag 52)
    """

    mu=398600 
    acc_vect=np.array([y_inner[1],-mu/(y_inner[0]*y_inner[0])])
    return acc_vect

def RK4(stateVector,h, time,output):
    """
    RK4 
    Note: no dependence on time
    """      
    yant=stateVector;
    y_vector=[]
    for t in np.arange(0, time,h):
        
        t0=t
        y0 = yant
        k0 = deriv(t0,y0)
        
        t1=t+0.5*h
        y1 = y0 + (0.5*h)*k0
        k1 = deriv(t1,y1)
        
        t2=t+0.5*h
        y2 = y0 + (0.5*h)*k1
        k2 = deriv(t2,y2)
        
        t3=t+h
        y3 = y0 + (h)*k2
        k3 = deriv(t3,y3)
        
        yfinal =  y0 + (1/6.0)*(k0+ k1*2 + k2*2 + k3)*h;
        yant = yfinal;
        y_vector.append(yfinal[0])
        output.write(str(t0)+' '+str(y0)+' '+str(k0)+'\n')
        output.write(str(t1)+' '+str(y1)+' '+str(k1)+'\n')
        output.write(str(t2)+' '+str(y2)+' '+str(k2)+'\n')
        output.write(str(t3)+' '+str(y3)+' '+str(k3)+'\n')

    return y_vector
    

def RK4_matrix(stateVector,h, time,output2):
    """
    RK compact
    s: stages of evaluation --> 4
    prueba
    """
    s=4 # Stages for RK4
    
    y_vector=[]
    # Coefficients
    a=np.array([0,1./2,1./2,1])
    b=np.array([[0,0,0],[1./2,0,0],[0,1./2,0],[0,0,1]])
    c=np.array([1./6,1./3,1./3,1./6])
    # init conditions
    yant= stateVector    
    for t in np.arange(0, time, h):
        k=[]
        phi=0
        for i in range(0,s):
            t_inner=t+a[i]*h
            y_inner = yant
            for j in range(0,i):
                y_inner = yant + h*b[i,i-1]*k[j];
            k.append(deriv(t_inner,y_inner))
            phi=phi+c[i]*k[i]
            output2.write(str(t_inner)+' '+str(y_inner)+' '+str(k[i])+'\n')
        yfinal=yant+h*phi
        y_vector.append(yfinal[0])
        yant = yfinal
    return y_vector


def RKF45(stateVector,t0,tf,output2):
    """
    RK - Fehlberg
    
    """
    s=6 # Stages for RKF45
    h=(tf-t0)/100.0
    h_vect=[]
    # Coefficients
    #a=np.array([0,1./4,3./8,12./13,1,1./2])
    b=np.array([[0,0,0,0,0],
                [1./4,0,0,0,0],
                [3./32,9./32,0,0,0],
                [1932./2197,-7200./2197,7296./2197,0,0],
                [439./216,-8,3680./513,-845./4104,0],
                [-8./27,2,-3544./2565,1859./4104,-11/40]])
    c_star=np.array([25./216,0,1408./2565,2197./4104,-1./5,0])
    c=np.array([16./135,0,6656./12825,28561./56430,-9./50,2./55])
    # init conditions
    yant= stateVector
    beta=0.8
    tol=1.0e-3
    t=t0
    t_out=[]
    y_out=[]
    v_out=[]
    while (t<tf):
        k=[]
        for i in range(0,s):
            y_inner = yant
            for j in range(0,i):
                y_inner = yant + h*b[i,i-1]*k[j];
            k.append(deriv(y_inner))
        # CONTROL ADAPTIVE STEP SIZE
        e_trunc=np.dot((c-c_star),k)
        e_scalar=max(np.abs(e_trunc))
        factor_h=(tol/e_scalar)**(1./5)
        if e_scalar <= tol:
            h = min(h,tf-t)
            t=t+h
            yfinal=yant+h*np.dot(c,k) # High 5
            yant=yfinal 
            t_out.append(t/60.0)
            y_out.append(yfinal[0])
            v_out.append(yfinal[1])
        h=min(h*beta*factor_h,4*h)
        h_vect.append(h)
        output2.write(str(t)+' '+str(yant)+' '+str(h)+'\n')
    return t_out,y_out, v_out, h_vect


        
if __name__=='__main__':
    
    """
    CURTIS - Example 1.20 - (pag 52)
    """
    import matplotlib.pyplot as plt
    import time
    start_time=time.time()
    outputXfile=open('check_120.txt','w')
    t0=0
    tf=70*60
    y=[6500,7.8]
    t_out,y_out, v_out, h_vect=RKF45(y,t0,tf,outputXfile)
    print(" %s seconds " % (time.time()-start_time))
    # PLOT
    x=np.arange(0,len(h_vect))
    plt.scatter(x,h_vect)
    #plt.scatter(t_out,y_out,s=0.1)
    #plt.scatter(t_out,v_out,s=0.1)
    plt.show()
    """
    CURTIS - Example 1.17 - (pag 46)
    """
    # import matplotlib.pyplot as plt
    # #output=open('checkFile.txt','w')
    # output2=open('checkFile2.txt','w')
    # stateVector=np.array([0,0])
    # ti=0
    # tf=110
    # h=1.0
    # #y_end=RK4(stateVector,h, tf,output)
    # y_end=RK4_matrix(stateVector,h, tf,output2)
    #
    # x=np.arange(ti,tf,h)
    # print(x)
    # print(y_end)
    # plt.plot(x,y_end)
    # plt.show()
    
        