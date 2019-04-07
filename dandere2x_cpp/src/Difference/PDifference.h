/*
 * P Difference generates the differences between two images using
 * predictive block matching, then saves the pixels of the missing (the parrts
 * that couldn't be found using predictive block matching), as well as the
 * meta data for the parts it could find.
 * 
 * By saving the metadata, it allows the merging aspect of Dandere2x to occur
 * later in execution. 
 */


//currently if entirely degenerate frame it crash

/* 
 * File:   PDifference.h
 * Author: linux
 *
 * Created on January 21, 2019, 6:41 PM
 */

#ifndef PDIFFERENCE_H
#define PDIFFERENCE_H
#include <memory>
#include <iostream>
#include <fstream>

#include "../Image/BlockMatch/DiamondSearch.h"
#include "../Image/Image/Image.h"
#include "../DandereUtils/DandereUtils.h"

#include "DifferenceBlocks.h"
#include "Inversion.h"



typedef DiamondSearch::point Point;

class PDifference {
public:


    int searchRadius = 80;
    int stepSize;
    int maxChecks;
    unsigned int blockSize;
    int width;
    int height;
    unsigned int bleed;
    double tolerance;
    bool debug;

    std::string pFrameFile;
    std::string inversionFile;
    
    
    std::vector<Block> blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    std::shared_ptr<Inversion> inv;
    Point disp;
    
    
    /**
     * 
     * @param image1 Stays the same
     * @param image2 is modified 
     * @param blockSize
     * @param bleed
     * @param tolerence
     * @param pFrameFile output for p-frame text file
     * @param inversionFile output for inversion text file
     * @param stepSize
     * @param debug
     * @return 
     */
    PDifference(
            std::shared_ptr<Image> image1,
            std::shared_ptr<Image> image2,
            unsigned int blockSize,
            int bleed,
            double tolerence,
            std::string pFrameFile,
            std::string inversionFile,
            int stepSize = 5,
            bool debug = true) {

        this->image1 = image1;
        this->image2 = image2;
        this->stepSize = stepSize;
        this->maxChecks = 128; //prevent diamond search from going on forever
        this->blockSize = blockSize;
        this->width = image1->width;
        this->height = image1->height;
        this->inv = nullptr;
        this->pFrameFile = pFrameFile;
        this->inversionFile = inversionFile;
        this->bleed = bleed;
        this->tolerance = tolerence;
        this->debug = true;

        //preform checks to ensure given information is valid
        if (image1->height != image2->height || image1->width != image2->width)
            throw std::invalid_argument("PDifference image resolution does not match!");

    }

    //no primative data types to cause memory leak
    ~PDifference(){
        
    }
    
    
    /*
     First, conduct a quick PSNR check between the two images.
     * If the PSNR is particularly bad, (i.e less than 60), just
     * assume it's a redraw.
     * 
     * 
     * second, if all the match blocks are larger than a set amount,
     * simply redraw the image
     
     */
    void generatePData() {
        double psnr = CImageUtils::psnr(*image1, *image2);

        if (psnr < 60) {
            std::cout << "PSNR is pretty low, not conducting match" << std::endl;
            blocks.clear();
        } else {
            matchAllBlocks();
        }

        int maxBlocks = (this->height * this->width) / (this->blockSize * this->blockSize);
        std::cout << "missing blocks: " << (maxBlocks - blocks.size()) << std::endl;



        //subtract block size from amount of missing blocks.
        //if this number is greater than the max desired blocks (i.e there's
        //a lot of missing blocks), decide whether to reject or accept
        if ((maxBlocks - blocks.size()) > (.85) * maxBlocks) {
            std::cout << " Missing blocks is 85 more than total image-"
                    "Initiating redraw. " << std::endl;
            blocks.clear();
        }

    }

    void save() {
        if (!blocks.empty()) { //if parts of frame2 can be made of frame1, create frame2'
            createInversion();
            
            this->inv->writeInversion(this->inversionFile);
            this->writePFrameData(this->pFrameFile);
        } 
        
        else { //if parts of frame2 cannot be made from frame1, just copy frame2. 
            
            this->inv->writeEmpty(this->inversionFile);
            this->printEmpty(this->pFrameFile);
        }
    }

    void forceCopy() {
        this->inv->writeEmpty(this->inversionFile);
        this->printEmpty(this->pFrameFile);
    }

    void createInversion() {
        inv = make_shared<Inversion>(blocks, blockSize, bleed, image2);
        inv->createInversion();
    }

    //for every block in frame1 and frame2, try and find a best match between the two. 

    void matchAllBlocks() {
        for (int x = 0; x < width / blockSize; x++) {
            for (int y = 0; y < height / blockSize; y++) {
                matchBlock(x, y);
            }
        }
    }


    //match block is the inner call within 'matchAlBlocks' for readibility and maintability.

    inline void matchBlock(int x, int y) {

        //initial disp is currently deprecated, but has ambitiouns to be introduced later.
        Point disp;
        disp.x = 0;
        disp.y = 0;

        double sum = CImageUtils::MSE(
                                           *image1,
                                           *image2,
                                           x * blockSize,
                                           y * blockSize,
                                           x * blockSize + disp.x,
                                           y * blockSize + disp.y,
                                           blockSize);

        //first we check if the blocks are in identical positions inbetween two frames.
        //if they are, we can skip doing a diamond search
        if (sum < tolerance) {
            blocks.push_back(Block(x * blockSize,
                                   y * blockSize,
                                   x * blockSize + disp.x,
                                   y * blockSize + disp.y, sum));
        }//if the blocks have been (potentially) displaced, conduct a diamond search to search for them. 
        else {
            //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
            Block result =
                    DiamondSearch::diamondSearchIterativeSuper(
                                                        *image2,
                                                        *image1,
                                                        x * blockSize + disp.x,
                                                        y * blockSize,
                                                        x * blockSize + disp.x,
                                                        y * blockSize + disp.y,
                                                        blockSize,
                                                        stepSize,
                                                        maxChecks);

            //if the found block is lower than the required PSNR, we add it. Else, do nothing
            if (result.sum < tolerance)
                blocks.push_back(result);
        }
    }

    /*
     Suppose frame1 (f1) and frame2 (f2) and f3 are the same image, but 
     * change 0.05 MSE each time. Suppose we allow a max of 0.06 MSE.
     * 
     * If we were to match f1 with f2, all is good. If we were to match
     * f2 with f3, we're in trouble. Since f2 in upscaled reality
     * is made out of pieces from f1, then the difference between f2
     * and f3 is actually 0.10, since f2 is actually made of f1.
     * 
     * As such, we need to use a new image, f2' (f2 prime) to compare
     * f2 to f3. f2' is the image of f2 from f1, and is made from drawing over.
     * 
     * We only draw over if it's required.  
     */
    void drawOverIfRequired() {
        if (!blocks.empty()) { //if parts of frame2 can be made of frame1, create frame2'
            drawOver();
        }
    }

    /**
     * 
     * WRites all data from a pFrame to a text fil
     * @param outputFile - Where the file will be saved
     */
    void writePFrameData(string outputFile) {
        std::ofstream out(outputFile + ".temp");
        for (int x = 0; x < blocks.size(); x++) {
            out << 
                    blocks[x].xStart << "\n" <<
                    blocks[x].yStart << "\n" <<
                    blocks[x].xEnd << "\n" <<
                    blocks[x].yEnd << endl;
        }

        rename((outputFile + ".temp").c_str(), outputFile.c_str());
        out.close();
    }


    //print an empty textfile to signal that this frame is neither
    //predicted or interpolated. 

    void printEmpty(string input) {
        std::ofstream out(input);
        out.close();
    }

    void drawOver() {
        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    image2->setColor(x + blocks[outer].xStart,
                                     y + blocks[outer].yStart,
                                    image1->getColorNoThrow(
                                            x + blocks[outer].xEnd,
                                            y + blocks[outer].yEnd));
                }
            }
        }
    }

    //    void save(std::string input, int compression = 100) {
    //
    //        unsigned int xBounds = image1->width;
    //        unsigned int yBounds = image1->height;
    //
    //        Image PFrame(xBounds, yBounds);
    //
    //        for (int outer = 0; outer < blocks.size(); outer++) {
    //            for (int x = 0; x < blockSize; x++) {
    //                for (int y = 0; y < blockSize; y++) {
    //                    PFrame.setColor(x + blocks[outer].xStart, y + blocks[outer].yStart,
    //                            image1->getColorNoThrow(x + blocks[outer].xEnd, y + blocks[outer].yEnd));
    //                }
    //            }
    //        }
    //
    //        PFrame.save(input.c_str(), compression);
    //
    //    }


    /**
     * Not used in final Dandere2x implementation. Leave in for debugging.
     */
    //    void generate(){
    //        if(!image1 || !image2)
    //            exit(1);
    //        
    //        matchAllBlocks();
    //    
    //        if(!blocks.empty()){ //if parts of frame2 can be made of frame1, create frame2'
    //            saveInversion(workspace + separator() + "outputs" + separator() + "output_" + std::to_string(frameNumber) + ".jpg");
    //            this->printPFrameData(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
    //            this->inv->printInversion(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
    //            overWrite();
    //            
    //            if(debug){
    //                this->save(workspace + separator() + "debug" + separator() + "debug_" + std::to_string(frameNumber) + ".jpg",30);
    //            }
    //        }
    //        
    //        else{ //if parts of frame2 cannot be made from frame1, just copy frame2. 
    //            image2->save(workspace + separator() + "outputs" + separator() + "output_" + std::to_string(frameNumber) + ".jpg");
    //            this->inv->printEmpty(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
    //            this->printEmpty(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
    //            
    //            if(debug)
    //                image2->save(workspace + separator() + "debug" + separator() + "debug_" + std::to_string(frameNumber) + ".jpg",30);
    //        }
    //
    //    }
    //    

    /**
     * 
     * 
     * DEPRECATED FUNCTIONS. THESE ARE VERY USEFUL!
     * 
     * matchBlockExhaustive will do a radius search
     * to find the canidate block rather than using diamond search
     **/
    //setDisp 

    /*Set Disp's goal is set a general displacement for predictive frames. It has worked kind
     of well, but is currently disabled due to it's herustical nature. 
      
     In other words, if there's a good chance that all the pixels were shifted by 10 down, then start
     all diamond searches 10 down. 
      
     */
    //    void setDisp(int startX, int startY) {
    //        searchRadius = 25;
    //        vector<Point> test = createSearchVector(startX, startY, 1920, 1080, searchRadius);
    //        vector <Block> blockSum = vector<Block>();
    //        
    //        //find initial disp
    //        for (int x = 0; x < test.size(); x++) {
    //            double average = CImageUtils::sumAverage(*image2, *image1, startX, startY, test[x].x, test[x].y,
    //                    blockSize); //seperate var for debugging
    //            blockSum.push_back(Block(startX, startY, test[x].x, test[x].y,
    //                    average));
    //        }
    //        
    //        auto smallestBlock = std::min_element(blockSum.begin(), blockSum.end());
    //        
    //        this->disp.x = startX - smallestBlock->xEnd;
    //        this->disp.y = startY - smallestBlock->yEnd;
    //        
    //        cout << disp.x << endl;
    //        cout << disp.y << endl;
    //        
    //    }

    //search vector for exhaustive searching about a region. Currently not used
    //due to slow preformance. 
    //    vector<Point> static createSearchVector(int centx, int centy, int maxx, int maxy, int maxBox) {
    //        
    //        vector<Point> list = vector<Point>();
    //        
    //        for (int x = centx - maxBox; x < centx + maxBox; x++) {
    //            for (int y = centy - maxBox; y < centy + maxBox; y++) {
    //                Point point;
    //                point.x = x;
    //                point.y = y;
    //                list.push_back(point);
    //            }
    //        }
    //        
    //        return list;
    //        
    //    }

    //     Block exhaustive(int startX, int startY) {
    //         searchRadius = 25;
    //         vector<Point> test = createSearchVector(startX, startY, 1920, 1080, searchRadius);
    //         vector <Block> blockSum = vector<Block>();
    //         
    //         //find initial disp
    //         for (int x = 0; x < test.size(); x++) {
    //             double average = CImageUtils::sumAverage(*image2, *image1, startX, startY, test[x].x, test[x].y,
    //                     blockSize); //seperate var for debugging
    //             blockSum.push_back(Block(startX, startY, test[x].x, test[x].y,
    //                     average));
    //         }
    //         
    //         auto smallestBlock = std::min_element(blockSum.begin(), blockSum.end());
    //         return *smallestBlock;
    //     }
    //     
    //     inline void matchBlockExhaustive(int x, int y){
    //         Point disp;  
    //         disp.x = 0;
    //         disp.y = 0;
    //         
    //         double sum = CImageUtils::sumAverage(*image1, *image2, x * blockSize, y * blockSize,
    //                 x * blockSize + disp.x, y * blockSize + disp.y, blockSize);
    //         
    //         //first we check if the blocks are in identical positions inbetween two frames.
    //         //if they are, we can skip doing a diamond search
    //         if (sum < 20) {
    //             blocks.push_back(Block(x * blockSize, y * blockSize, x * blockSize + disp.x,
    //                     y * blockSize + disp.y, sum));
    //         } 
    //         
    //         //if the blocks have been (potentially) displaced, conduct a diamond search to search for them. 
    //         else {
    //             //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
    //             Block result = exhaustive(x*blockSize + disp.x,y*blockSize + disp.y);
    //             
    //             //if the found block is lower than the required PSNR, we add it. Else, do nothing
    //             if (result.sum < 20) 
    //                 blocks.push_back(result);
    //         }
    //     } 


private:


};

#endif /* PDIFFERENCE_H */

