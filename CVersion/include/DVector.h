#ifndef FVECTOR_H
#define FVECTOR_H


class DVector
{
    private:
        double* vec;
        unsigned asize;
    public:
        DVector();
        DVector(unsigned asize);
        DVector(double* vec, unsigned asize);
        DVector(const DVector &other);
        double& operator[](unsigned index);
        const DVector operator+(const DVector &other)const;
        DVector& operator+=(const DVector &other);
        DVector& operator=(const DVector &other);
        const DVector operator*(double val)const;
        virtual ~DVector();
};

#endif // FVECTOR_H
