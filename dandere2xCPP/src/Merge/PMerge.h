#ifndef PMERGE_H
#define PMERGE_H

#include <memory>
#include <iostream>
#include <fstream>
#include <vector>

#include "../Image/Block.h"
#include "../Image/VectorDisplacement.h"
#include "../DandereUtil/DandereUtils.h"
#include "../Image/Image/Image.h"

/*
 PMerge is the class that pieces together information once everything 
 * is completed, i.e waifu2x has scaled all the outputs produced by
 * 'PDifference', and saves it in the respective directory. 
 */


class PMerge {
public:
    
    
    /*
     These vectors are the inputs, line by line, from the inversion_data
     * and pframe_data files. Once we have all the information
     * in the text file saved into a vector, we put them into vector
     * displacements so we can remerge them back into the program later.
     */
    std::vector<std::string> vectorDisplacementsText;
    std::vector<VectorDisplacement> vectorDisplacements;
    
    std::vector<std::string> inversionDisplacementsText;
    std::vector<VectorDisplacement> inversionDisplacements;
    
    
    /*
     * Base large refers to the previous image that we will be drawing over. 
     * inversionLarge refers to the upscaled image of differences that
     * needs to be stitched over baseLarge.
     */
    std::shared_ptr<Image> baseLarge;
    std::shared_ptr<Image> inversionLarge;
    Image output;
    
    std::string workspace;
    int frameNumber;
    int blockSize;
    int bleed;
    
    PMerge(std::string workspace, int frameNumber, int blockSize, int bleed){
        this->workspace = workspace;
        this->vectorDisplacementsText = readFile(workspace + separator() + "pframe_data" + separator() + "pframe_" + std::to_string(frameNumber) + ".txt");
        this->inversionDisplacementsText = readFile(workspace + separator() + "inversion_data" + separator() + "inversion_" + std::to_string(frameNumber) + ".txt");
        this->frameNumber = frameNumber;
        this->blockSize = blockSize;
        this->bleed = bleed;
        
        //create vector displacements from the vectorDisplacementsText. It's intuitive how this works:
        //line 0-3 refers to the first displacement, 3-7 refers to second, etc etc. 
        for(int x = 0; x < vectorDisplacementsText.size()/4; x++){
            vectorDisplacements.push_back(VectorDisplacement(std::stoi(vectorDisplacementsText[x*4]),std::stoi(vectorDisplacementsText[x*4 + 1]),
                    std::stoi(vectorDisplacementsText[x*4 + 2]), std::stoi(vectorDisplacementsText[x*4 +3])));
        }
        
        for(int x = 0; x < inversionDisplacementsText.size()/4; x++){
            inversionDisplacements.push_back(VectorDisplacement(std::stoi(inversionDisplacementsText[x*4]),std::stoi(inversionDisplacementsText[x*4 + 1]),
                    std::stoi(inversionDisplacementsText[x*4 + 2]), std::stoi(inversionDisplacementsText[x*4 +3])));
        }
        
        baseLarge = std::make_shared<Image>(workspace + separator() + "merged" + separator() + "merged_" + std::to_string(frameNumber) + ".jpg");
        inversionLarge = std::make_shared<Image>(workspace + separator() + "upscaled" + separator() + "upscaled_" + std::to_string(frameNumber) + ".png");
        output = Image(baseLarge->width,baseLarge->height);
        
    }
    
    std::vector<std::string> readFile(string input){
        std::ifstream file(input.c_str());
        std::string str;
        std::vector<std::string> readFile;
        while (std::getline(file, str))
            readFile.push_back(str);
        
        return readFile;
    }
    
    void saveMerge(){
        
        
        //If there is no information in vectorDisplacement and inversions,
        //that means we're dealing with a non-predicted and non-interpolated frame,
        //in other words, needs to be entirely redrawn. So in this case,
        //just copy the file over. 
        if(vectorDisplacements.empty() && inversionDisplacements.empty()){
            inversionLarge->save(workspace + separator() + "merged" + separator() + "merged_" + std::to_string(frameNumber + 1) + ".jpg",50);
            return;
        }
        
        
        /*
         * Copy over all the changes that are recycled in previous frame.
         * For example, if block 25x 72y gets shifted to 25x 73y, shift
         * over that block. 
         */
        for (int outer = 0; outer < vectorDisplacements.size(); outer++) {
            for (int x = 0; x < blockSize*2; x++) {
                for (int y = 0; y < blockSize*2; y++) {
                    output.setColor(x + 2*vectorDisplacements[outer].x,y + 2*vectorDisplacements[outer].y,
                            baseLarge->getColorNoThrow(x + 2*vectorDisplacements[outer].newX ,y + 2*vectorDisplacements[outer].newY));
                }
            }
        }
        
        
        /*
         Copy over the missing information that wasn't shifted in the predictive / interpolated
         * generated from inversion. It's hard to articulate how this works, read
         * inversion class to understand what's going on more. 
         */
        for(int outer = 0; outer < inversionDisplacements.size(); outer++){
            for (int x = 0; x < (blockSize * 2); x++) {
                for (int y = 0; y < (blockSize * 2); y++) {
                    output.setColor(inversionDisplacements[outer].x*2 + x, inversionDisplacements[outer].y*2 + y,
                            inversionLarge->getColor(inversionDisplacements[outer].newX * (2 * (blockSize + bleed)) + x + bleed, inversionDisplacements[outer].newY * (2 * (blockSize + bleed)) + y + bleed));
                    
                }
            }   
        }
        output.save(workspace + separator() + "merged" + separator() + "merged_" + std::to_string(frameNumber + 1) + ".jpg",80);
    }
    
    
    //    PMerge(const PMerge& orig);
    //    virtual ~PMerge();
private:
    
};

#endif /* PMERGE_H */

