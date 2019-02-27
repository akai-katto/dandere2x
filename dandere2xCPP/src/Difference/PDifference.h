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
#include "../Image/DiamondSearch.h"
#include "../Image/DifferenceBlocks.h"
#include "../DandereUtil/DandereUtils.h"
#include "../DandereUtil/PreSetup.h" //create folder
#include "../Image/Image/Image.h"
#include "Inversion.h"



typedef DiamondSearch::point Point;




class PDifference {
public:
    //PDifference(const PDifference& orig);
    ~PDifference(){
        //inversion.reset();
    }
    
    int searchRadius = 80;
    int stepSize;
    int maxChecks; 
    unsigned int blockSize;
    int width;
    int height;
    unsigned int frameNumber;
    unsigned int bleed;
    double tolerance;
    bool debug; 
    
    
    std::string workspace;
    std::vector<Block> blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    std::shared_ptr<char> workDir;
    std::shared_ptr<Inversion> inv;
    Point disp;
 
    PDifference(std::shared_ptr<Image> image1,
                std::shared_ptr<Image> image2,
                int frameNumber,
                unsigned int blockSize,
                int bleed,
                double tolerence,
                std::string workspace,
                int stepSize = 5, 
                bool debug = true){
        
        this->image1 = image1;
        this->image2 = image2;
        this->stepSize = stepSize; 
        this->maxChecks = 128; //prevent diamond search from going on forever
        //this->workDir = workDir;
        this->blockSize = blockSize;
        this->width = image1->width;
        this->height = image1->height;
        this->inv = nullptr;
        this->frameNumber = frameNumber;
        this->workspace = workspace;
        this->bleed = bleed;
        this->tolerance = tolerence;
        this->debug = true;
        
        
        //preform checks to ensure given information is valid
        if(image1->height != image2->height || image1->width != image2->width)
            throw std::invalid_argument("PDifference image resolution does not match!");
        
    }
    
    PDifference(std::string workspace, 
    unsigned int blockSize,
    int bleed,
    double tolerence,
    int stepSize = 5, 
    bool debug = true){
        this->stepSize = stepSize; 
        this->maxChecks = 128; //prevent diamond search from going on forever
        this->blockSize = blockSize;
        this->inv = nullptr;
        this->frameNumber = 0;
        this->workspace = workspace;
        this->bleed = bleed;
        this->tolerance = tolerence;
        this->debug = true;
    }
    
    void setNewFrame(int frameNumber, std::shared_ptr<Image> image1, 
                    std::shared_ptr<Image> image2){
        this->frameNumber = frameNumber;
        this->image1 = image1;
        this->image2 = image2;
        blocks.empty();
        
        this->width = image1->width;
        this->height = image1->height;
        
        //preform checks to ensure given information is valid
        if(image1->height != image2->height || image1->width != image2->width)
            throw std::invalid_argument("PDifference image resolution does not match!");
    }
    
    
    void generate(){
        if(!image1 || !image2)
            exit(1);
        
        matchAllBlocks();
    
        if(!blocks.empty()){ //if parts of frame2 can be made of frame1, create frame2'
            saveInversion(workspace + separator() + "outputs" + separator() + "output_" + std::to_string(frameNumber) + ".jpg");
            this->printPFrameData(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
            this->inv->printInversion(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
            overWrite();
            
            if(debug){
                this->save(workspace + separator() + "debug" + separator() + "debug_" + std::to_string(frameNumber) + ".jpg",30);
            }
        }
        
        else{ //if parts of frame2 cannot be made from frame1, just copy frame2. 
            image2->save(workspace + separator() + "outputs" + separator() + "output_" + std::to_string(frameNumber) + ".jpg");
            this->inv->printEmpty(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
            this->printEmpty(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
            
            if(debug)
                image2->save(workspace + separator() + "debug" + separator() + "debug_" + std::to_string(frameNumber) + ".jpg",30);
        }

    }
    
    void generatePData(){
        if(!image1 || !image2)
            exit(1);
        
        matchAllBlocks();

        if(!blocks.empty()){ //if parts of frame2 can be made of frame1, create frame2'
            saveInversion(workspace + separator() + "outputs" + separator() + "output_" + std::to_string(frameNumber) + ".jpg");
            this->printPFrameData(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
            this->inv->printInversion(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");

            std::cout << "before overwrite " << endl;
            overWrite();
            
        }
        else{ //if parts of frame2 cannot be made from frame1, just copy frame2. 
            this->inv->printEmpty(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
            this->printEmpty(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
        }
        
    }
    
    void saveInversion(string input){
        inv = make_shared<Inversion>(blocks, blockSize,bleed, image2);
        inv->createInversion();
        //inv->saveInversion(input);
    }
    
    
    
    //for every block in frame1 and frame2, try and find a best match between the two. 
    void matchAllBlocks(){
        for (int x = 0; x < width / blockSize; x++) {
            for (int y = 0; y < height / blockSize; y++) {
               matchBlock(x,y);
            }
        }
    }
    
                
    //match block is the inner call within 'matchAlBlocks' for readibility and maintability.
    inline void matchBlock(int x, int y){
        
        //initial disp is currently deprecated, but has ambitiouns to be introduced later.
        Point disp;  
        disp.x = 0;
        disp.y = 0;


        double sum = CImageUtils::sumAverage(*image1, *image2, x * blockSize, y * blockSize,
                x * blockSize + disp.x, y * blockSize + disp.y, blockSize);

        //first we check if the blocks are in identical positions inbetween two frames.
        //if they are, we can skip doing a diamond search
        if (sum < tolerance) {

            blocks.push_back(Block(x * blockSize, y * blockSize, x * blockSize + disp.x,
                    y * blockSize + disp.y, sum));
  
        } 
        //if the blocks have been (potentially) displaced, conduct a diamond search to search for them. 
        else {
     
            //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
            Block result = DiamondSearch::diamondSearchIterativeSuper(
                    *image2,
                    *image1,
                    x * blockSize+ disp.x,
                    y * blockSize,
                    x * blockSize + disp.x,
                    y * blockSize + disp.y, blockSize,
                    stepSize,
                    maxChecks);
            
            //if the found block is lower than the required PSNR, we add it. Else, do nothing
            if (result.sum < tolerance) 
                blocks.push_back(result);
        }
    }
    
    



    //print pframe data to a text file so 
    //it can be used by PMerge in an other execution
    void printPFrameData(string input){
        std::ofstream out(input);
        for(int x = 0; x < blocks.size(); x++){
            out << blocks[x].xStart << "\n" <<  blocks[x].yStart << "\n" <<
                    blocks[x].xEnd << "\n" << blocks[x].yEnd << endl;
        }
	out.close(); 
    }
    
    
    //print an empty textfile to signal that this frame is neither
    //predicted or interpolated. 
    void printEmpty(string input){
        std::ofstream out(input);
	out.close(); 
    }
    
    
    /*
     * We call PDifferences using pointers to CImages. 
     * Whenever we create a predictive frame, it's important
     * we modify the image in question to prevent subtle changes from going
     * unnoticed.
     * 
     * To articulate that - suppose we're given frame1, frame2, frame3.
     * 
     * frame1 and frame2 have subtle differences, but it's neglible.
     * so we create frame2 out of frame1, denoted frame2' (frame2 prime)
     * 
     * If we used frame2 to create frame3', there's a problem that
     * perhaps there's some difference in frame2 and frame2' that causes issues.
     * 
     * Perhaps parts of frame3' would differ if we used frame2' than just frame2,
     * since frame2' is actually made of frame1. 
     * 
     * In other words, we need to keep track of our changes, because
     * while frame2' may look like frame2, it may cause a butterfly
     * effect in the future. 
    */
    void overWrite(){
        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    image2->setColor(x + blocks[outer].xStart,y + blocks[outer].yStart,
                            image1->getColorNoThrow(x + blocks[outer].xEnd ,y + blocks[outer].yEnd));
                }
            }
        }
    }
        
     void save(std::string input, int compression = 100) {
        
        unsigned int xBounds = image1->width;
        unsigned int yBounds = image1->height;
        
        Image PFrame(xBounds, yBounds);
        
        for (int outer = 0; outer < blocks.size(); outer++) {
            for (int x = 0; x < blockSize; x++) {
                for (int y = 0; y < blockSize; y++) {
                    PFrame.setColor(x + blocks[outer].xStart,y + blocks[outer].yStart,
                            image1->getColorNoThrow(x + blocks[outer].xEnd ,y + blocks[outer].yEnd));
                }
            }
        }
        
        PFrame.save(input.c_str(),compression);
        
    }
    
    
   
    
    
     
     /**
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

