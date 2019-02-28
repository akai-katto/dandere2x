/*
 Essentially just a datastructure to maintain displacements.
 
 * This could be a structure, but having a constructor is too nice. 
 * Future developments plan on having this be readable from an object / writable
 */
#ifndef VECTORDISPLACEMENT_H
#define VECTORDISPLACEMENT_H

class VectorDisplacement {
public:
    int x;
    int y;
    int newX;
    int newY;

    VectorDisplacement(int x, int y, int newX, int newY) {
        this->x = x;
        this->y = y;
        this->newX = newX;
        this->newY = newY;
    }




};

#endif /* VECTORDISPLACEMENT_H */

