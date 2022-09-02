#ifndef ATYPES_H_INCLUDED
#define ATYPES_H_INCLUDED

#include <map>
#include "DVector.h"

typedef DVector(*fper)(DVector&, std::map<string, string>& arguments);



#endif // ATYPES_H_INCLUDED
