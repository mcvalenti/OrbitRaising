'''
Created on 26 sep. 2021

@author: ceci
'''
import numpy as np



class Propagator(object):
    '''
    classdocs
    '''  
    
    def __init__(self, *args, **kwargs):
        
        super().__init__()
        self.mu = 398600.448
        self.stateVectors = []
        self.h = kwargs['step']
        self.stateVector = kwargs['stateVector']
        
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

                
        fig = plt.figure()
        ax = plt.axes(projection='3d')        
        plt.title("Orbita Propagada RK4  - cuerpo central")
        ax.plot3D(x, y, z, 'gray')
        plt.show()
        
        
    def __deriv(self, stateVector,perturb_funcs):
        """
        Computes acceleration vector from perturbation functions.
        -----------------------------------------------------------
        output: acc_vector np.array [km/s2]
        """
        
        acc_vector=np.array([0,0,0])
        for f in perturb_funcs:
            acc_vector=acc_vector+f(stateVector)
        
        result = np.array([ stateVector[3],
                            stateVector[4],
                            stateVector[5],
                            acc_vector[0],
                            acc_vector[1],
                            acc_vector[2],
                           ]) 

        return result;
        
        
    def RK4(self, time,funcs):
        """
        RK4 
        """
        
        yant     = self.stateVector;
        for t in range(0, time, self.h):
            
            y0 = yant
            k0 = self.__deriv(y0,funcs)
            
            y1 = y0 + (0.5*self.h)*k0
            k1 = self.__deriv(y1,funcs)
            
            y2 = y0 + (0.5*self.h)*k1
            k2 = self.__deriv(y2,funcs)
            
            y3 = y0 + (self.h)*k2
            k3 = self.__deriv(y3,funcs)
            
            yfinal =  y0 + (1/6.0)*(k0+ k1*2 + k2*2 + k3)*self.h;

            self.stateVectors.append(yfinal)
            yant = yfinal;
            
    def get_svs(self):
        return self.stateVectors

    