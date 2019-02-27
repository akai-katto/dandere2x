//
// Header file for DiamondSearch.cpp
//

#ifndef LODEPNG_DIAMONDSEARCH_H
#define LODEPNG_DIAMONDSEARCH_H

#include <vector>
#include <algorithm>    // std::sort

#include "Block.h"
#include "Image/Image.h"
#include "Image/Image.h"
#include "Image/ImageUtils.h"

using namespace std;
class DiamondSearch {
    
public:
    struct point {
        int x;
        int y;
    };
    
    static bool flagInvalidPoints(int xBounds, int yBounds, point points[], int size, bool flagged[]){
        
        int count = 0;
        for (int i = 0; i < size; i++) {
            if ((points[i].x > xBounds) || (points[i].x < 0) ||
                    (points[i].y > yBounds) || (points[i].y < 0)) {
                flagged[i] = true;
                count++;
            }
        }
        
        return count != size;
    }
    
    
    static Block diamondSearchIterative(Image &imageA,
    Image &imageB, int initialX, int initialY,
    int xOrigin, int yOrigin, int boxSize, int stepSize, int max){
        
        int xBounds = imageA.width;
        int yBounds = imageA.height;
        
        double sum;
        
        std::vector<Block> blocks = std::vector<Block>();
        
        
        //create the points to be used in diamond searching
        point pointArray[8];
        
        for (int x = 0; x < max; x++) {
            
            blocks.clear();
            //if we ran out of moves
            if (x == max) {
                double sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, xOrigin, yOrigin, boxSize);
                return Block(initialX, initialY, xOrigin, yOrigin, sum);
            }
            
            //if step size is 0 we cannot continue
            if (stepSize <= 0) {
                double sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, xOrigin, yOrigin, boxSize);
                return Block(initialX, initialY, xOrigin, yOrigin, sum);
            }
            
            
            //construct the list of "diamond" points to be checked if legal or not
            pointArray[0].x = xOrigin + stepSize;
            pointArray[0].y = yOrigin;
            
            pointArray[1].x = xOrigin + stepSize / 2;
            pointArray[1].y = yOrigin + stepSize / 2;
            
            pointArray[2].x = xOrigin;
            pointArray[2].y = yOrigin + stepSize;
            
            pointArray[3].x = xOrigin - stepSize / 2;
            pointArray[3].y = yOrigin + stepSize / 2;
            
            pointArray[4].x = xOrigin - stepSize;
            pointArray[4].y = yOrigin;
            
            pointArray[5].x = xOrigin + stepSize / 2;
            pointArray[5].y = yOrigin - stepSize / 2;
            
            pointArray[6].x = xOrigin + stepSize;
            pointArray[6].y = yOrigin;
            
            pointArray[7].x = xOrigin;
            pointArray[7].y = yOrigin;
            
            
            
            //Create an array that is used to signal if a point is "valid" or not, i.e if it is legal to visit.
            //In other words, we need to know the index of an array is allowed or not.
            
            bool flagArray[8] = {true};
            bool anyLegalPoints = flagInvalidPoints(xBounds, yBounds, pointArray,8, flagArray);
            
            //flag invalid points returns a boolean if there are no valid points for diamond search to visit
            //therfore, return a 'null' block, (a block with a really high PSNR (peak signal to noise ratio), so it
            //will be ignored by the rest of the system
            if (!anyLegalPoints) //if the entire
                return Block(0, 0, 0, 0, 99999);
            
            
            
            //cycle through each point (if it's legal that is) and add it to the block vector.
            for (int i = 0; i < 8; i++) {
                if (!flagArray[i]) {
                    
                    sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, pointArray[i].x, pointArray[i].y,
                            boxSize);
                    
                    Block block = Block(initialX, initialY, pointArray[i].x, pointArray[i].y, sum);
                    blocks.push_back(block);
                    
                }
            }
            
            
            //get the most promising block from the list (the one with the smallest 'sum'
            std::vector<Block>::iterator smallestBlock = min_element(blocks.begin(), blocks.end());
            
            
            if ((smallestBlock->xEnd == xOrigin) && smallestBlock->yEnd == yOrigin) {
                xOrigin = smallestBlock->xEnd;
                yOrigin = smallestBlock->yEnd;
                max--;
                stepSize /= 2;
                continue;
            }
            
            xOrigin = smallestBlock->xEnd;
            yOrigin = smallestBlock->yEnd;
            max--;
        }
    }
    
    static Block diamondSearchIterativeSuper(Image &imageA,
    Image &imageB, int initialX, int initialY,
    int xOrigin, int yOrigin, int boxSize, int stepSize, int max){
        
        int xBounds = imageA.width;
        int yBounds = imageA.height;
        
        double sum;
        
        std::vector<Block> blocks = std::vector<Block>();
        
        
        //create the points to be used in diamond searching
        point pointArray[15];
        
        for (int x = 0; x < max; x++) {
            
            blocks.clear();
            //if we ran out of moves
            if (x == max) {
                double sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, xOrigin, yOrigin, boxSize);
                return Block(initialX, initialY, xOrigin, yOrigin, sum);
            }
            
            //if step size is 0 we cannot continue
            if (stepSize <= 0) {
                double sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, xOrigin, yOrigin, boxSize);
                return Block(initialX, initialY, xOrigin, yOrigin, sum);
            }
            
            
            //construct the list of "diamond" points to be checked if legal or not
            pointArray[0].x = xOrigin + stepSize;
            pointArray[0].y = yOrigin;
            
            pointArray[1].x = xOrigin + stepSize / 2;
            pointArray[1].y = yOrigin + stepSize / 2;
            
            pointArray[2].x = xOrigin;
            pointArray[2].y = yOrigin + stepSize;
            
            pointArray[3].x = xOrigin - stepSize / 2;
            pointArray[3].y = yOrigin + stepSize / 2;
            
            pointArray[4].x = xOrigin - stepSize;
            pointArray[4].y = yOrigin;
            
            pointArray[5].x = xOrigin + stepSize / 2;
            pointArray[5].y = yOrigin - stepSize / 2;
            
            pointArray[6].x = xOrigin + stepSize;
            pointArray[6].y = yOrigin;
            
            pointArray[7].x = xOrigin;
            pointArray[7].y = yOrigin;
            
            pointArray[8].x = xOrigin + stepSize*2;
            pointArray[8].y = yOrigin;
            
            pointArray[9].x = xOrigin + stepSize;
            pointArray[9].y = yOrigin + stepSize;
            
            pointArray[10].x = xOrigin;
            pointArray[10].y = yOrigin + stepSize*2;
            
            pointArray[11].x = xOrigin - stepSize;
            pointArray[11].y = yOrigin + stepSize;
            
            pointArray[12].x = xOrigin - stepSize*2;
            pointArray[12].y = yOrigin;
            
            pointArray[13].x = xOrigin + stepSize;
            pointArray[13].y = yOrigin - stepSize;
            
            pointArray[14].x = xOrigin + stepSize*2;
            pointArray[14].y = yOrigin;
            
            
            
            
            //Create an array that is used to signal if a point is "valid" or not, i.e if it is legal to visit.
            //In other words, we need to know the index of an array is allowed or not.
            
            bool flagArray[15] = {true};
            bool anyLegalPoints = flagInvalidPoints(xBounds, yBounds, pointArray,14, flagArray);
            
            //flag invalid points returns a boolean if there are no valid points for diamond search to visit
            //therfore, return a 'null' block, (a block with a really high PSNR (peak signal to noise ratio), so it
            //will be ignored by the rest of the system
            if (!anyLegalPoints) //if the entire
                return Block(0, 0, 0, 0, 99999);
            
            
            
            //cycle through each point (if it's legal that is) and add it to the block vector.
            for (int j = 0; j < 15; j++) {
                
                if (!flagArray[j]) {
                    sum = CImageUtils::sumAverage(imageA, imageB, initialX, initialY, pointArray[j].x, pointArray[j].y,
                            boxSize);
                    
                    Block block = Block(initialX, initialY, pointArray[j].x, pointArray[j].y, sum);
                    blocks.push_back(block);
                    
                }
            }
            
            
            //get the most promising block from the list (the one with the smallest 'sum'
            std::vector<Block>::iterator smallestBlock = min_element(blocks.begin(), blocks.end());
            
            
            if ((smallestBlock->xEnd == xOrigin) && smallestBlock->yEnd == yOrigin) {
                xOrigin = smallestBlock->xEnd;
                yOrigin = smallestBlock->yEnd;
                max--;
                stepSize /= 2;
                continue;
            }
            
            //        if(smallestBlock->sum < 5){
            //            return *smallestBlock;
            //        }
            
            xOrigin = smallestBlock->xEnd;
            yOrigin = smallestBlock->yEnd;
            max--;
        }
    }
    
    
};


#endif //LODEPNG_DIAMONDSEARCH_H