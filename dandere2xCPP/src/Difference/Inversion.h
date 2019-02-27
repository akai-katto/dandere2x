/*
 * Inversion is a subtask of PDifference (as it passes itself as an object)
 * that's been seperated from PDifference due to it's specific
 * function and maintainability.
 * 
 * Inversions goal is given an image like this:
 * Given this image here(hopefully it's not deprecated) https://i.imgur.com/mAXjgtK.jpg,
 * 
 * Find all the black boxes, record their locations, create a new image
 * for all the black boxes, and save that image along side with it's
 * 
 * original positions. 
 * 
 * 
 * More documentation is expected in the near future. 
 */

/* 
 * File:   Inversion.h
 * Author: linux
 *
 * Created on January 22, 2019, 6:47 PM
 */

#ifndef INVERSION_H
#define INVERSION_H

#include "../Image/DifferenceBlocks.h"
#include "../Image/Block.h"
#include <memory>
#include <math.h>  
#include <vector>
#include <iostream>
#include <fstream>

#include "../Image/Image/Image.h"

class Inversion {
public:
  
    std::vector<std::vector<bool>> occupiedPixel;
    std::vector<Block> blocks;
    int blockSize;
    std::shared_ptr<DifferenceBlocks> invDifferences;
    std::shared_ptr<Image> frame2;
    int bleed;
    
    Inversion(std::vector<Block> &blocks, int blockSize, int bleed, std::shared_ptr<Image> frame2){
        this->blocks = blocks;
        this->blockSize = blockSize;
        this->frame2 = frame2;
        this->bleed = bleed;
                //initialize 2d bool array for createInverse()
//        this->occupiedPixel = new bool*[this->frame2->width];
//        
//        for(int i = 0; i < this->frame2->width; i++)
//            this->occupiedPixel[i] = new bool[this->frame2->height];
            
            
    }
        
    Inversion(const Inversion& orig);
    
    ~Inversion(){
    }
    


    void createInversion(){
        //pre conditions
        if(blocks.empty())
            throw std::invalid_argument("p frame must be created before creating inversion");
        
        occupiedPixel.resize(1920,std::vector<bool>(1080));
        //flag all the pixels that already exist within predictive_frame2
        for(int outer = 0; outer < blocks.size(); outer++){
            for(int x = 0; x < blockSize; x++){
                for(int y = 0; y < blockSize; y++){
                    occupiedPixel[blocks[outer].xStart + x][blocks[outer].yStart + y] = true;
                }
            }
        }
        
        
        //count how many pixels need to be redrawn
        int count = 0;
        for(int x = 0; x < frame2->width; x++){
            for(int y = 0; y < frame2->height; y++){
                if(occupiedPixel[x][y]==false)
                    count++;
            }
        }
        
        count /= blockSize*blockSize; //find out how many blocks need to be redrawn 
        int dimensions = (int) sqrt(count) + 1;  //let this be the dimensions for our output image
        
        
        
        //create an object to organize the output image (see reading on DifferenceBlocks)
        invDifferences = std::make_unique<DifferenceBlocks>(dimensions*(blockSize + bleed),
                dimensions*(blockSize + bleed), blockSize + bleed);
        
        
        //
        for(int x = 0; x < frame2->width; x++){
            for(int y = 0; y < frame2->height; y++){
                if(occupiedPixel[x][y]==false){
                    invDifferences->add(x,y); //add to the inversions
                    
                    //set the pixels to 'draw' so we don't redraw it twice
                    for(int deltax = 0; deltax < blockSize; deltax++){
                        for(int deltay =0; deltay < blockSize; deltay++){
                            occupiedPixel[x + deltax][y + deltay] = true;
                        }
                    }
                }
            }
        }       
        
    }
    
    void saveInversion(std::string input){
        if(!invDifferences)
            throw std::invalid_argument("inversions is null, cannot save");

        Image out = Image(invDifferences->xDimension, invDifferences->yDimension);
        
        
        //using the blocks generated from invDifferences, save the image
        for (int outer = 0; outer <  invDifferences->list.size() ; outer++) {
            for (int x = 0; x < (blockSize + bleed); x++) {
                for (int y = 0; y < (blockSize + bleed); y++) {
                            
                    out.setColor(
                            invDifferences->list[outer].newX * (blockSize+bleed) + x,
                            invDifferences->list[outer].newY * (blockSize+bleed) + y,
                            frame2->getColorNoThrow(invDifferences->list[outer].x  + x - bleed/2,
                            invDifferences->list[outer].y + y - bleed/2));
                    
                }
            }
        }
        
        out.save(input);
    }
    
    
    void printEmpty(std::string input){
        std::ofstream out(input);
	out.close(); 
    }
    void printInversion(std::string input){
        std::ofstream out(input);
        for(int x = 0; x < invDifferences->list.size(); x++){
            out << invDifferences->list[x].x << "\n" <<  invDifferences->list[x].y << "\n" <<
                    invDifferences->list[x].newX << "\n" << invDifferences->list[x].newY << std::endl;
        }
	out.close(); 
    }
    
    void printInversionFacts(){
        int sizeInv = invDifferences->xDimension * invDifferences->yDimension;
        int sizeOg = frame2->width * frame2->height;
        double percentage = sizeInv / sizeOg;
        std::cout << "P efficiency: " << percentage << endl;
    }
private:

};

#endif /* INVERSION_H */

