/*
 * This is a bit of a read. This is used in the "Inversion" class, and seeks to 
 * simplify an open problem in Dandere2x.
 * 
 * Given this image here(hopefully it's not deprecated) https://i.imgur.com/mAXjgtK.jpg,
 * notice all the black parts. We refer to these as the 'differences'.
 * 
 * We need to get all the 'differences' in a way it can be upscaled. So what's the 
 * opposite of this image? The inversion!
 * 
 * See how all the blocks are sometimes disjoint but sometimes connected? Well, 
 * we need to have all the missing blocks in an image, somehow.
 * 
 * So what we do, if we know how many blocks there are, say there's N blocks,
 * 
 * is create a new image of sqrt(n) by sqrt(n) size, and then fill
 * in all the blocks into that image!
 * 
 * We start from the top left, slowly adding the missing blocks left to right,
 * then once we reach the limit, we goto the next row. We do this over and
 * over again until it's finished.
 */

/* 
 * File:   DifferenceBlocks.h
 * Author: linux
 *
 * Created on December 16, 2018, 11:41 PM
 */

#ifndef DIFFERENCEBLOCKS_H
#define DIFFERENCEBLOCKS_H

#include "VectorDisplacement.h"
#include <vector>

class DifferenceBlocks {
    
public:
    int size;
    int xMax;
    int yMax;
    int xCount;
    int yCount;
    int xDimension;
    int yDimension;
    std::vector<VectorDisplacement> list = std::vector<VectorDisplacement>();
    
    
    DifferenceBlocks(int xDimension, int yDimension, int size){
        this->xDimension = xDimension;
        this->yDimension = yDimension;
        this->xMax = xDimension /size;
        this->yMax = yDimension / size;
        this->xCount = 0;
        this->yCount = 0;
        this->size = size;
    }
    
    void add(int x, int y){
        size++;
        if(xCount + 1 < xMax){
            xCount++;
            list.push_back(VectorDisplacement(x,y,xCount,yCount));
            //xCount++;
        }
        else{
            yCount++;
            xCount = 0;
            list.push_back(VectorDisplacement(x,y,xCount,yCount));
            
        }
    }
};

#endif /* DIFFERENCEBLOCKS_H */

