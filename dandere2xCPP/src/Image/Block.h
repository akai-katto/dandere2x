
/*
 * 
 * Kind of like the vector displacement class, but contains
 * a sum so it can be sorted by DiamondSearch or ExhaustiveSearch.
 * 
 */

//
// Created by linux on 11/13/18.
//

#ifndef LODEPNG_BLOCK_H
#define LODEPNG_BLOCK_H
#include <iostream>


class Block {
public:
    int xStart;
    int yStart;
    int xEnd;
    int yEnd;
    double sum;
    Block(int xStart, int yStart, int xEnd, int yEnd, double sum){
        this->xStart = xStart;
        this->yStart = yStart;
        this->xEnd = xEnd;
        this->yEnd = yEnd;
        this->sum = sum;
    }
    
    Block(int xStart, int yStart, int xEnd, int yEnd){
        this->xStart = xStart;
        this->yStart = yStart;
        this->xEnd = xEnd;
        this->yEnd = yEnd;
    }
    
    Block(const Block& other){

        this->xStart = other.xStart;
        this->yStart = other.yStart;
        this->xEnd = other.xEnd;
        this->yEnd = other.yEnd;
        this->sum = other.sum;
    }

    bool operator<(const Block &other){
        return this->sum < other.sum;
    }


    //for creating displacement vector files
    friend std::ostream& operator<<(std::ostream& os, Block& block) {
        return os << block.xStart <<  block.yStart  << block.xEnd << block.yEnd<<"\n";
    }

};


#endif //LODEPNG_BLOCK_H
