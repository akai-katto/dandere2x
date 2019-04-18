#ifndef CORRECTION_H
#define CORRECTION_H

#include <memory>
#include <iostream>
#include <fstream>

#include "../Image/Image/Image.h"
#include "../Image/BlockMatch/DiamondSearch.h"
#include "../DandereUtils/DandereUtils.h"

/**
 Description: 
 * 
 * Given frames A' and A where A' is a prediction of A 
 * using blocks of size N, try fixing the issues of A' by
 * using block matches of sqrt(N) size on A' to bring
 * A' closer to A.
 */
class Correction {
public:
    int stepSize;
    int maxChecks;
    unsigned int blockSize;
    int width;
    int height;
    unsigned int bleed;
    double tolerance;
    std::string correctionFile;
    bool debug;

    std::vector<Block> blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    Point disp;

    Correction(std::shared_ptr<Image> image1,
            std::shared_ptr<Image> image2,
            unsigned int blockSize,
            int bleed,
            double tolerence,
            std::string correctionFile,
            int stepSize,
            bool debug = true) {

        this->image1 = image1;
        this->image2 = image2;
        this->stepSize = stepSize;
        this->maxChecks = 64; //prevent diamond search from going on forever
        this->blockSize = blockSize;
        this->width = image1->width;
        this->height = image1->height;
        this->correctionFile = correctionFile;
        this->bleed = bleed;
        this->tolerance = tolerence;

        //preform checks to ensure given information is valid
        if (image1->height != image2->height || image1->width != image2->width)
            throw std::invalid_argument("PDifference image resolution does not match!");

    }

    void matchAllBlocks() {
        for (int x = 0; x < width / blockSize; x++) {
            for (int y = 0; y < height / blockSize; y++) {
                matchBlock(x, y);
            }
        }
    }

    inline void matchBlock(int x, int y) {

        //initial disp is currently deprecated, but has ambitiouns to be introduced later.
        Point disp;
        disp.x = 0;
        disp.y = 0;

        double sum = ImageUtils::MSE(*image1, *image2, x * blockSize, y * blockSize,
                x * blockSize + disp.x, y * blockSize + disp.y, blockSize);

        //std::cout << sum << std::endl;

        if (sum < tolerance) {
            //blocks.push_back(Block(x * blockSize, y * blockSize, x * blockSize + disp.x,
              //      y * blockSize + disp.y, sum));

        }//if the blocks have been (potentially) displaced, conduct a diamond search to search for them. 
        else {
            //std::cout << "Conducting a diamond search" << std::endl;
            //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
            Block result = DiamondSearch::diamondSearchIterativeSuper(
                    *image2,
                    *image1,
                    x * blockSize + disp.x,
                    y * blockSize,
                    x * blockSize + disp.x,
                    y * blockSize + disp.y,
                    blockSize,
                    stepSize,
                    maxChecks);

            //std::cout << "Tolerance: " << result.sum << std::endl;

            //if the found block is lower than the required PSNR, we add it. Else, do nothing
            if (result.sum < tolerance ) {
                //std::cout << "matched block" << std::endl;
                blocks.push_back(result);
            }
        }
    }

    void drawOver() {
        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    image1->setColor(
                            x + blocks[outer].xStart,
                            y + blocks[outer].yStart,
                            image1->getColorNoThrow(x + blocks[outer].xEnd,
                                                    y + blocks[outer].yEnd));
                }
            }
        }
    }

    void writeCorrection() {
        std::ofstream out(this->correctionFile + ".temp");
        for (int x = 0; x < blocks.size(); x++) {
            out <<  blocks[x].xStart << "\n" <<
                    blocks[x].yStart << "\n" <<
                    blocks[x].xEnd << "\n" <<
                    blocks[x].yEnd << endl;
        }

        rename((this->correctionFile + ".temp").c_str(), this->correctionFile.c_str());
        out.close();
    }

    void writeEmpty() {
        std::ofstream out(this->correctionFile);
        out.close();
    }


};
#endif