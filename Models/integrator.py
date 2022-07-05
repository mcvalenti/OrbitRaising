'''
Created on 5 jul. 2022

@author: ceci
'''

class integrator(object):
    '''
    Numerical integrator of general derivatives 1D
    '''


    def __init__(self,  *args, **kwargs):
        '''
        fderiv: derivative function to be integrated
        x_init: variable initial condition
        y_init: function initial condition
        step: step for the integration
        '''
        super().__init__()
    
        self.x_init = kwargs['x_init']
        self.x_fin = kwargs['x_fin']
        self.y_init = kwargs['y_init']
        self.h = kwargs['step']
        self.y_values=[]
        
        
    def fderiv(self,x_init,y_init):
        """Particular function"""
        return x_init+y_init-1
        
    
    def RK4(self):
        """
        RK4 
        """
        for x in range(int(self.x_init*10),int(self.x_fin*10), int(self.h*10)):
            
            x=x/10.0
            y0=self.y_init
            k0 = self.fderiv(x,y0)
            
            y1 = y0 + 0.5*self.h*k0
            k1 = self.fderiv(x+0.5*self.h,y1)
            
            y2 = y0 + 0.5*self.h*k1
            k2 = self.fderiv(x+0.5*self.h,y2)
            
            y3 = y0 + self.h*k2
            k3 = self.fderiv(x+self.h,y3)
            
            yfinal =  y0 + (self.h/6.0)*(k0+ k1*2 + k2*2 + k3);
    
            self.y_values.append(yfinal)
            y0 = yfinal;
        print (x)   
        return {}
    
    def AdamsBashford(self,x_pred, y_pred):
        """ Predictor and corrector method
            y_init_vect: the previous values coputed with RK4
        """
        y_3=y_pred[3]
        yp_3=self.fderiv(x_pred[3],y_pred[3])
        yp_2=self.fderiv(x_pred[2],y_pred[2])
        yp_1=self.fderiv(x_pred[1],y_pred[1])
        yp_0=self.fderiv(x_pred[0],y_pred[0])
        #Predictor
        y_star_4=y_3+(self.h/24)*(55*yp_3-59*yp_2+37*yp_1-9*yp_0)
        print(y_star_4)
        yp_4=self.fderiv(self.x_fin,y_star_4)
        #Corrector
        y_4=y_3+(self.h/24)*(9*yp_4+19*yp_3-5*yp_2+yp_1)
        print(y_4)
        return {}
    
if __name__ == "__main__":
    
    import numpy as np
    int1=integrator(x_init=0,x_fin=0.8,y_init=1,step=0.2)
    int1.RK4()
    print (int1.y_values)
    x_pred=np.array([0,0.2,0.4,0.6])
    y_pred=np.array([1,1.0214, 1.06568, 1.10996])
    int1.AdamsBashford(x_pred, y_pred)
    print ((0.8*0.8)/2+np.exp(0.8)-0.8)
    
    
    
