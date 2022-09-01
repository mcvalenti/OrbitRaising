'''
Created on 17 jul. 2022

Propagations that includes mass into the State Vector
in order to be able to compute finite maneuvers

@author: ceci
'''

import numpy as np



class Propagator(object):
    '''
    classdocs
    '''  
    
    def __init__(self, *args, **kwargs):
        """
        stateVector= x,y,z,vx,vy,vz,m
        """        
        super().__init__()
        self.mu = 398600.448
        self.stateVectors = []
        self.h = kwargs['step'] # in seconds
        self.stateVector = kwargs['stateVector']
        self.mass=kwargs['mass']
        self.thrust=kwargs['thrust']
        self.isp=kwargs['isp']
        
    
        
    def plot(self):
        
        from mpl_toolkits import mplot3d
        import matplotlib.pyplot as plt
        x = []
        y = []
        z = []
        
        for e in self.stateVectors:
            x.append(e[0])
            y.append(e[1])
            z.append(e[2])

                
        ax = plt.axes(projection='3d')        
        plt.title("Orbita Propagada RK4  - cuerpo central")
        ax.plot3D(x, y, z, 'orange')
        plt.show()
        
        
    def __deriv(self, stateVector,perturb_funcs):
        """
        Computes acceleration vector from perturbation functions.
        -----------------------------------------------------------
        output: acc_vector np.array [km/s2] + mass consumption
        """
        
        acc_vector=np.array([0,0,0,0])
        for f in perturb_funcs:
            acc_vector=acc_vector+f(statevector=stateVector,thrust=self.thrust,isp=self.isp)
        
        result = np.array([ stateVector[3],
                            stateVector[4],
                            stateVector[5],
                            acc_vector[0],
                            acc_vector[1],
                            acc_vector[2],
                            acc_vector[3],
                           ]) 

        return result;
        
        
    def RK4(self, time,funcs):
        """
        RK4 
        """
        
        yant= self.stateVector;
        for t in np.arange(0, time, self.h):
            
            h=self.h
            y0 = yant
            k0 = self.__deriv(y0,funcs)
            
            y1 = y0 + (0.5*h)*k0
            k1 = self.__deriv(y1,funcs)
            
            y2 = y0 + (0.5*h)*k1
            k2 = self.__deriv(y2,funcs)
            
            y3 = y0 + (h)*k2
            k3 = self.__deriv(y3,funcs)
            
            yfinal =  y0 + (1/6.0)*(k0+ k1*2 + k2*2 + k3)*h;

            self.stateVectors.append(yfinal)
            yant = yfinal;
            
    def get_svs(self):
        return self.stateVectors
    
    def last_sv(self):
        return self.stateVectors[-1]

def r_v_Dtheta(r0,v0,Dtheta):
    """
    Computes r,v from r0,v0 and Delta Theta
    theta: true anomaly
    Dtheta: Delta Theta, from Theta0 to Theta [rad]
    """
    mu=398600.448 # km3/s2
    # Initial computations
    r0_mod=np.linalg.norm(r0)
    v0_mod=np.linalg.norm(v0)
    vr0=np.dot(r0,v0)/r0_mod # Radial Velocity
    h=r0_mod*np.sqrt(v0_mod*v0_mod-vr0*vr0) # Angular momentum
 
    
    # r
    denominator=1+((h*h/(mu*r0_mod))-1)*np.cos(Dtheta)-h*vr0*np.sin(Dtheta)/mu
    r=(h*h)/(mu*denominator)

    
    # Lagrange Coefficients
    f=1-(mu*r)*(1-np.cos(Dtheta))/(h*h)
    g=r*r0_mod*np.sin(Dtheta)/h
    paren=mu*(1-np.cos(Dtheta))/(h*h)-(1/r0_mod)-(1/r)
    f_dot=mu*(1-np.cos(Dtheta))/(h*np.sin(Dtheta))*paren
    g_dot=1-(mu*r0_mod/(h*h))*(1-np.cos(Dtheta))
    
    # Finally, r, v
    
    r_f=f*r0+g*v0
    v_f=f_dot*r0+g_dot*v0
    
    return r_f,v_f

def xv2eo(r,v):
        """
        ---------------------------------------------
        Trasformacion de vector de estado x,v
        a elementos orbitales.
        ---------------------------------------------
        inputs:
            x: posicion (vector) - [km]
            v: velocidad (vector) - [km/s]
        outputs:
            a: semieje mayor (float) - [km]
            e: excentricidad (float)
            i: inclinacion (float) - [rad]
            Omega: Longitud del Nodo (float) - [rad]
            w: Argumento del perigeo (float) - [rad]
            nu: Anomalia verdadera (float) - [rad]
        """
    #    Rt=6378.0 #[km]
        GM=398600.4405 #[km3/s2]
        deg=180.0/np.pi 
    #    rad=np.pi/180.0

        rmod=np.sqrt(np.dot(r,r))
        vmod=np.sqrt(np.dot(v,v))
        """
        i,Omega
        """
        h=np.cross(r,v)
        hmod=np.linalg.norm(h)
        h=np.dot(1./hmod,h)
        i=np.arctan(np.sqrt(h[0]*h[0]+h[1]*h[1])/h[2])
        if i < 0.0:
            i=np.pi+i
        if h[1]!=0:    
            arg=-h[0]/h[1]
            Omega=np.arctan(arg)
            if np.sign(-h[1]) < 0.0:
                Omega=Omega+np.pi
        else:
            Omega=0
    
        # Radial velocity
        vr=np.dot(r,v)/rmod
    
        """
         e
        """
        # e vector
        e_vect=(1/GM)*((vmod*vmod-(GM/rmod))*r-rmod*vr*v)
        # e modulus
        e=np.linalg.norm(e_vect)
        """
         a
        """
         
        a=hmod*hmod/(GM*(1-e*e))
        

        """
         M    
        """
        E=np.arctan((np.dot(r,v)/(a*a*a))/(1-rmod/a))
        if np.sign((1-rmod/a)) < 0.0:
            E=E+np.pi
        M=E-e*np.sin(E)
    
        """
         w, nu
        """
        w=0 # Not interested for this exercise
         
        if vr>=0:
            nu=np.arccos(np.dot(e_vect/e,r/rmod))
        else:
            nu=2*np.pi-np.arccos(np.dot(e_vect/e,r/rmod))
        
        """
        Impresion de salida
        """
    #     print 'semieje mayor a= ',a
    #     print 'Excentricidad e= ',e
    #     print 'Inclinacion i= ',i*deg
    #     print 'Longitud del Nodo = ', Omega*deg
    #     print 'Argumento del Perigeo w= ',w*deg
    #     print 'Anomalia Media ',M*deg
    #     print 'Anomalia Verdadera',nu*deg
        return a,e,i,Omega,w,nu
    
if __name__ == '__main__':
    
    #----------------------
    # funcion xv2eo
    #----------------------
    r=np.array([-6045,-3490,2500])
    v=np.array([-3.457,6.618,2.533])
    a,e,i,Omega,w,nu=xv2eo(r,v)
    print(e,nu*180.0/np.pi)
    
    #----------------------
    # function r_v_Dtheta
    #----------------------
    # deg2rad=np.pi/180.0
    # r0=np.array([8182.4,-6865.9])
    # v0=np.array([0.47572,8.8116])
    # Dtheta=120*deg2rad
    #
    # r,v=r_v_Dtheta(r0, v0, Dtheta)
    # print (r,v)
    
    
    
    