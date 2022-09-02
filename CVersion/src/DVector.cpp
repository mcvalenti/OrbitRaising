#include "DVector.h"
#include <string.h>
#include <stdexcept>

DVector::DVector()
{
    this->vec = NULL;
    this->asize = 0;
    //ctor
}

DVector::DVector(double* vec, unsigned asize)
{
    this->vec = new double[asize];
    this->asize = asize;
    //ctor
    memcpy(this->vec, vec, asize*sizeof(vec[0]));
}

DVector::DVector(unsigned asize)
{
    this->vec = new double[asize];
    this->asize = asize;
    //ctor

}

DVector::DVector(const DVector &other)
{
    this->vec = new double[other.asize];
    this->asize = other.asize;
    //ctor
    memcpy(this->vec, other.vec, other.asize*sizeof(vec[0]));
}

const DVector DVector::operator+(const DVector &other)const{
    DVector result(other.asize);
    for(unsigned i=0;i<this->asize;i++){
        result.vec[i] = this->vec[i] + other.vec[i];
    }
    return result;
}


DVector& DVector::operator=(const DVector &other){

    delete [] this->vec;
    this->vec = new double[other.asize];
    this->asize = other.asize;

    memcpy(this->vec, other.vec, asize*sizeof(vec[0]));
    return *this;
}


DVector& DVector::operator+=(const DVector &other){

    if(other.asize!=this->asize)
        throw std::runtime_error("out of bounds");

    for(unsigned i=0;i<this->asize;i++){
        this->vec[i] += other.vec[i];
    }
    return *this;
}


const DVector DVector::operator*(double val)const{
    DVector result(this->asize);
    for(unsigned i=0;i<this->asize;i++){
        result.vec[i] = this->vec[i] * val;
    }
    return result;
}

double& DVector::operator[](unsigned index){
    if(index>asize-1){
        throw std::runtime_error("out of bounds");
    }
    return this->vec[index];
}




DVector::~DVector()
{
    //dtor
    delete [] this->vec;
}
