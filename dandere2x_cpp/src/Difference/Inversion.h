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

#include "DifferenceBlocks.h"
#include "../Image/BlockMatch/Block.h"
#include "../Image/Image/Image.h"

#include <memory>
#include <math.h>  
#include <vector>
#include <iostream>
#include <fstream>

class Inversion {
public:

    std::vector<std::vector<bool>> occupiedPixel;
    std::vector<Block> blocks;
    std::shared_ptr<DifferenceBlocks> invDifferences;
    std::shared_ptr<Image> frame2;


    int blockSize;
    int bleed;
    int height;
    int width;
    int blocksNeeded;
    int dimensions;
    
    Inversion(std::vector<Block> &blocks, int blockSize, int bleed, std::shared_ptr<Image> frame2) {
        this->blocks = blocks;
        this->blockSize = blockSize;
        this->frame2 = frame2;
        this->bleed = bleed;

        this->height = frame2->height;
        this->width = frame2->width;

    }

    Inversion(const Inversion& orig);

    ~Inversion() {
    }

    void createInversion() {
        flagPixels();
        
        //once flagPixels is called, count how many pixels didn't get flagged
        int count = countEmptyPixels();
        
        //find out how many blocks are needed to redraw all the missing pixels
        int blocksNeeded = count / (blockSize*blockSize);
        
        //let this be the dimensions for our output image
        this->dimensions = (int) sqrt(blocksNeeded) + 1; 
        
        //using the new information we have, add all the missing blocks
        //into invDifferences
        addMissingBlocksInvDifferences();

    }

    /**
     * 
     * Suppose we're given an image that looks like this
     * 
     * abcd f
     * ghijkl
     * mn pqr
     * stu wx
     * 
     * And let the various letters represent pixels. In a 'pframe', there are
     * pixels that are missing that cannot be reproduced. In this case, they
     * are e,o, and v.
     * 
     * We need to flag which pixels are missing from the image so we can put
     * those missing pixels into a new image to be upscaled.
     */
    void flagPixels() {
        //we create a 2d vector called (occupied pixels) which
        //determines which pixels are vacent.
        this->occupiedPixel.resize(this->width, std::vector<bool>(this->height));

        //flag all the pixels that already exist within predictive_frame2
        //so we can decide what pixels are missing
        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    this->occupiedPixel[blocks[outer].xStart + x][blocks[outer].yStart + y] = true;
                }
            }
        }
    }
    
    
    /**
     * Suppose we're given an image that looks like this
     * 
     * abcd f
     * ghijkl
     * mn pqr
     * stu wx
     * 
     * we need to know how many of the pixels are missing in order to 
     * create a new image to be upscaled. This simply counts
     * how many are missing, in this image, 3.
     * 
     * @return 
     */

    int countEmptyPixels() {
        //count how many pixels need to be redrawn
        int count = 0;
        for (int x = 0; x < frame2->width; x++) {
            for (int y = 0; y < frame2->height; y++) {
                if (occupiedPixel[x][y] == false)
                    count++;
            }
        }
        return count;
    }

     /**
      * We change our example image to something more appropriate.
      * Let the 'blocksize' of this image be '2'. 
      * 
      * aabbcc  ee
      * aabbcc  ee
      * ffgghhiijj
      * ffgghhiijj
      * kk  mmnnoo
      * kk  mmnnoo
      * ppqq  sstt
      * ppqq  sstt
      * 
      * 
      * Once can see there's two  missing blocks. From countEmptyPixels,
      * we know how many blocks are missing from the image, it's just a matter
      * of getting those pixels into a new image to be upscaled. In this case,
      * there are 3 missing blocks.
      * 
      * Using the invDifferences object, we traverse through the entire image.
      * Starting at (0,0), no th is isn't missing. (0,2), nope. (0,7), yes
      * this is missing.
      * 
      * We add (0,7) and it's respective block into invDifferences (see object
      * class for more specifications), then we flag all the pixels
      * at the block in order to not double add the image. So after adding the
      * block to invDifferences and flagging the pixels, our image looks like
      * this.
      * 
      * aabbccxxee
      * aabbccxxee
      * ffgghhiijj
      * ffgghhiijj
      * kk  mmnnoo
      * kk  mmnnoo
      * ppqq  sstt
      * ppqq  sstt
      * 
      * So we marked that block as 'added'.
      * 
      * the invDifferences has the data neccecary to create an image
      * that now looks like this:
      * 
      * dd--  
      * dd--
      * ----
      * ----
      * 
      * After we repeat the process for the entire image, the 'flagged' image
      * will be competely filled in like this,
      * 
      * aabbccxxee
      * aabbccxxee
      * ffgghhiijj
      * ffgghhiijj
      * kkxxmmnnoo
      * kkxxmmnnoo
      * ppqqxxsstt
      * ppqqxxsstt
      * 
      * 
      * and our invDifferences 'image' (invDifferences only hold vectors,
      * but we can still symbolically draw the contents)
      * 
      * ddll
      * ddll
      * ss--
      * ss--
      * 
      * Using this 'invDifferences' image, we have all the pieces
      * needed to recreate the entire image.
     *
     * 
     * @return 
     */
    void addMissingBlocksInvDifferences() {
                //create an object to organize the output image (see reading on DifferenceBlocks)
        invDifferences = std::make_unique<DifferenceBlocks>(dimensions * (blockSize + bleed),
                dimensions * (blockSize + bleed), blockSize + bleed);
        
        //now that we have a list of every pixel that needs to be redrawn
        for (int x = 0; x < frame2->width; x++) {
            for (int y = 0; y < frame2->height; y++) {
                if (occupiedPixel[x][y] == false) {
                    invDifferences->add(x, y); //add to the inversions

                    //set the pixels to 'draw' so we don't redraw it twice
                    for (int deltax = 0; deltax < blockSize; deltax++) {
                        for (int deltay = 0; deltay < blockSize; deltay++) {
                            occupiedPixel[x + deltax][y + deltay] = true;
                        }
                    }
                }
            }
        }
    }

    void writeEmpty(std::string input) {
        std::ofstream out(input);
        out.close();
    }

    void writeInversion(std::string outputFile) {
        std::ofstream out(outputFile + ".temp");
        for (int x = 0; x < invDifferences->list.size(); x++) {
            out << invDifferences->list[x].x << "\n" << invDifferences->list[x].y << "\n" <<
                    invDifferences->list[x].newX << "\n" << invDifferences->list[x].newY << std::endl;
        }
        rename((outputFile + ".temp").c_str(), outputFile.c_str());
        out.close();
    }

    //    void saveInversion(std::string input) {
    //        if (!invDifferences)
    //            throw std::invalid_argument("inversions is null, cannot save");
    //
    //        Image out = Image(invDifferences->xDimension, invDifferences->yDimension);
    //
    //
    //        //using the blocks generated from invDifferences, save the image
    //        for (int outer = 0; outer < invDifferences->list.size(); outer++) {
    //            for (int x = 0; x < (blockSize + bleed); x++) {
    //                for (int y = 0; y < (blockSize + bleed); y++) {
    //
    //                    out.setColor(
    //                            invDifferences->list[outer].newX * (blockSize + bleed) + x,
    //                            invDifferences->list[outer].newY * (blockSize + bleed) + y,
    //                            frame2->getColorNoThrow(invDifferences->list[outer].x + x - bleed / 2,
    //                            invDifferences->list[outer].y + y - bleed / 2));
    //
    //                }
    //            }
    //        }
    //
    //        out.save(input);
    //    }


private:

};

#endif /* INVERSION_H */

