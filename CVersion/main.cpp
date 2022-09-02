#include <iostream>
#include <list>
using namespace std;

#include "atypes.h"
#include "DVector.h"
#include "perturb.h"
#include "RK4.h"
int main()
{
    list<fper> lf;
    /*
    double v1[] = {1,2,3,4,5};
    DVector vec1(v1, sizeof(v1)/sizeof(v1[0]));
    DVector vec2(v1, sizeof(v1)/sizeof(v1[0]));
    DVector vec3(vec2);
    DVector* vec4 = new DVector(v1, sizeof(v1)/sizeof(v1[0]));
    */
    //at_SV=np.array([])
    double v[] = {6858,0,0,0,7.7102,0,2000};
    try{
        DVector stateVector(v, sizeof(v)/sizeof(v[0]));
        RK4 rg(stateVector, 1, 2000, 1000, 300);

        lf.push_back(perturvacionNula);
        rg.run(5400, lf);


    }catch(exception& e){
        cout<<e.what()<<endl;
    }

    cout << "Hello world!" << endl;
    return 0;
}
