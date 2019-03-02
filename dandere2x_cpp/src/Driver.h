/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   Driver.h
 * Author: linux
 *
 * Created on February 9, 2019, 5:45 PM
 */

#ifndef DRIVER_H
#define DRIVER_H

#include "DandereUtils/DandereUtils.h" //waitForFile
#include "Difference/PDifference.h"


/**
 * 
 * 1) In Dandere2x, the first frame of any function is seen as different.
 * Reiterating, parts of frame1 can exists in parts of frame2, frame5, or frame1000.
 * 
 * That is to say, every frame preceding frame1 can possibely have parts derived
 * from frame1. As a result, we load frame1 seperate from the rest,
 * and continually make modifications as we go.
 * 
 * 
 * 2) Given two frames and the data required to start finding differences, 
 * compute the differences between two frames. 
 * 
 * 3) Read comment method for this. We need to draw over the previous frame
 * 
 * 4) Assign drawn over frame as the new base frame. 
 * 
 * @param workspace
 * @param frameCount
 * @param blockSize
 * @param tolerance
 * @param stepSize
 */
void driverDifference(std::string workspace, int frameCount, int blockSize, double tolerance, int stepSize){
    
    
    int bleed = 2;
    bool debug = true;
    
    //1 
    waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + ".jpg");
    shared_ptr<Image> im1 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + ".jpg");
    
    for(int x = 1; x < frameCount; x++){
        waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        std::cout << "Computing differences for frame" << x << endl;
        shared_ptr<Image> im2 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        PDifference dif = PDifference(im1, im2,x, blockSize,bleed, tolerance, workspace, stepSize, debug);
        dif.generatePData(); //2
        dif.drawOverIfRequired(); //3
        im1 = im2; //4

    }
    
}



void driverDifferenceResume(std::string workspace,int resumeCount, int frameCount, int blockSize, double tolerance, int stepSize){
    
    
    int bleed = 2;
    bool debug = true;
    
    //1 
    waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(resumeCount) + ".jpg");
    shared_ptr<Image> im1 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(resumeCount) + ".jpg");
    
    for(int x = resumeCount; x < frameCount; x++){
        waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        std::cout << "Computing differences for frame" << x << endl;
        shared_ptr<Image> im2 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        PDifference dif = PDifference(im1, im2,x, blockSize,bleed, tolerance, workspace, stepSize, debug);
        if(x==resumeCount){
            std::cout << "invoking force copy " << endl;
            dif.forceCopy();
            im1 = im2;
            continue;
        }
        dif.generatePData(); //2
        dif.drawOverIfRequired(); //3
        im1 = im2; //4

    }
    
}





#endif /* DRIVER_H */

