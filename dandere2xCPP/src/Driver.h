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

#include "DandereUtil/PreSetup.h"
#include "DandereUtil/DandereUtils.h"
#include "Difference/PDifference.h"
#include "Merge/PMerge.h"


void driverDifference(std::string workspace, int frameCount, int blockSize, double tolerance, int stepSize){
    
    int bleed = 2;
    bool debug = true;
    
    waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + ".jpg");
    shared_ptr<Image> im1 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + ".jpg");
    
    for(int x = 1; x < frameCount; x++){
        waitForFile(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        std::cout << "Computing differences for frame" << x << endl;
        shared_ptr<Image> im2 = make_shared<Image>(workspace + separator() + "inputs" + separator() + "frame" + to_string(x+1) + ".jpg");
        PDifference dif = PDifference(im1, im2,x, blockSize,bleed, tolerance, workspace, stepSize, debug);
        dif.generatePData();
        im1 = im2;

    }
    
}

void driverMerge(std::string workspace, int frameCount){
    int bleed = 2;
    int blockSize = 30;
    
    for(int x = 1; x < frameCount; x++){
        PMerge mergetest = PMerge(workspace, x, blockSize, bleed);
        mergetest.saveMerge();
    }
    
}



#endif /* DRIVER_H */

