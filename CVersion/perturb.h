#ifndef PERTURB_INCLUDED
#define PERTURB_INCLUDED


#include "DVector.h"
//Debe respetar prototipo/firma
//typedef DVector(*fper)(DVector&,int, int);
//Retorna un DVector y recibe un DVector y 2 enteros.
//Si los parametros son variables se debe implementar lista o diccionario

DVector central_body(DVector& stateVector, double a, double b);
DVector thrust_force(DVector& stateVector, double a, double b);
#endif // PERTURB_INCLUDED
