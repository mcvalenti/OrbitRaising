#ifndef PERTURB_INCLUDED
#define PERTURB_INCLUDED
#include <map>

#include "DVector.h"
//Debe respetar prototipo/firma
//typedef DVector(*fper)(DVector&,int, int);
//Retorna un DVector y recibe un DVector y 2 enteros.
//Si los parametros son variables se debe implementar lista o diccionario

DVector central_body(DVector& stateVector, std::map<string, string>& arguments);
DVector thrust_force(DVector& stateVector, std::map<string, string>& arguments);
#endif // PERTURB_INCLUDED
