#ifndef RK4_H
#define RK4_H

using namespace std;
#include <list>
#include "../atypes.h"

#include "DVector.h"

#define MU              398600.448
#define STATEVECTORSIZE 7

#include <stdio.h>
class RK4
{

    private:
        DVector stateVector;
        std::map<string, string> arguments;
        std::list<DVector> stateVectors;
        int step;
        double mass;
        int thrust;
        int isp;

    public:
        RK4(const DVector& stateVector, int step=1, double mass=200, double thrust=1000.0, double isp=300.0);
        DVector __deriv(DVector& stateVector, std::list<fper>& funcs);
        DVector run(int time, std::list<fper>& perturb_funcs);
        virtual ~RK4();
        int saveToStream(FILE* ostream);
        void consoleShow();

};

#endif // RK4_H
