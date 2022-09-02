#include "math.h"
#include "perturb.h"

#define CUAD(X) (X)*(X)

DVector thrust_force(DVector& stateVector, double a, double b){

    /*
    Computes thrust forces and mass consumption
    input: stateVector_mass [array, dim:7] - The state vector considers
            the satellite mass
    output : acceleration vector for each components [km2/s] and
            mass consumption
    */
    DVector result(4);
    double thrust   =   a;
    double isp      =   b;
    const double g0 =   9.81; //# [km/s2]
    double v_mod;
    double coeff;

    v_mod=sqrt(CUAD(stateVector[3])+CUAD(stateVector[4])+CUAD(stateVector[5]));

    coeff=thrust/(stateVector[6]*v_mod*1000);// # (1000) Thrust aligned with velocities [km/s2]

    result[0] = stateVector[3]*coeff;
    result[1] = stateVector[4]*coeff;
    result[2] = stateVector[5]*coeff;
    result[3] = -thrust/(isp*g0);

    return result;

}


DVector central_body(DVector& stateVector, double a, double b){
    /*
    """
    Computes gravity acelerations of central body force
    input: stateVector [array]
    output: aceleration vector for each components [km2/s]
    """
    */
    const double GM = 398600.448f;
    double r;
    double coeff;
    DVector r_vect(3);
    DVector resultado(4);

    r = stateVector[0]*stateVector[0] +
        stateVector[1]*stateVector[1] +
        stateVector[2]*stateVector[2];

    r = sqrt(r);
    coeff = -(GM)/pow(r,3);

    resultado[0] = stateVector[0]*coeff;
    resultado[1] = stateVector[1]*coeff;
    resultado[2] = stateVector[2]*coeff;
    resultado[3] = 0;
    return resultado;

}
