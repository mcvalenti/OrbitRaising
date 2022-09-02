#include "RK4.h"

#include <string.h>



RK4::RK4(const DVector& stateVector, int step, double mass, int thrust, int isp)
{
    this->stateVector  = stateVector;

    this->step = step;
    this->mass = mass;
    this->thrust = thrust;
    this->isp = isp;
    //ctor
}



//Optimizar para evitar retornar copia!!!
DVector RK4::__deriv(DVector& stateVector, std::list<fper>& perturb_funcs){
    DVector accVector(4);
    DVector result;
    for(fper f:perturb_funcs){
        //acc_vector=acc_vector+f(statevector=stateVector,thrust=self.thrust,isp=self.isp)

        //Para mejorar rendimiendo usamos vectores planos
        accVector+=f(stateVector, this->thrust, this->isp);

    }

    result[0] = stateVector[3];
    result[1] = stateVector[4];
    result[2] = stateVector[5];

    result[3] = accVector[0];
    result[4] = accVector[1];
    result[5] = accVector[2];
    result[6] = accVector[3];
    return result;
}



void RK4::run(int time, std::list<fper>& funcs){
    DVector yant, y0, k0, y1, k1, y2, k2, y3, k3, yfinal;
    int h = this->step;
    yant = this->stateVector;

    for(int t=0;t<time;t+=this->step){
        //step = this->step;
        //entender, muy ineficiente copias y copias
        y0   = yant;
        k0   = this->__deriv(y0, funcs);

        y1   = y0 + k0*(0.5*h);
        k1   = this->__deriv(y1,funcs);

        y2 = y0 + k1*(0.5*h);
        k2 = this->__deriv(y2,funcs);

        y3 = y0 + k2*h;
        k3 = this->__deriv(y3,funcs);

        yfinal =  y0 + (k0+(k1*2)+(k2*2)+k3)*h*(1/(float)6.0);

        this->stateVectors.push_back(yfinal);
            //self.stateVectors.append(yfinal)
        yant = yfinal;

    }



}

RK4::~RK4()
{
    //dtor
    //delete this->stateVector;
}
