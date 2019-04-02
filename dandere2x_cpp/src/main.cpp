
/**
 * TODO
 * 
 * - Add logging to c++ module
 * - Refine c++ edge cases a bit more
 * - Comment
 * 
 **/


#include <string>
#include <iostream>
#include <cstdlib>
#include <chrono>

#include "Difference/PDifference.h"
#include "Driver.h" //driverDifference
#include "Image/Image/Image.h"
#include "Image/Image/ImageUtils.h"
using namespace std;


//note to readers,
//I plan on re-organizing Dandere2xCpp as I have a better idea of how I want
//the project to be organized as I move into the future.

//FutureList:
//-CLI
//-Subproccesses
//-More heuristics

int main(int argc, char** argv){
    bool debug = false; //debug flag
    
    string workspace = "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\";
    int frameCount = 2000;
    int blockSize = 30;
    double tolerance = 15;
    double psnrMax = 98;
    double psnrMin = 94;
    int stepSize = 4;
    string runType = "n";// 'n' or 'r'
    int resumeFrame = 23;
    string extensionType = ".jpg";
    
    if(!debug){
        workspace = argv[1];
        frameCount = stoi(argv[2]); 
        blockSize = atoi(argv[3]);
        tolerance = stod(argv[4]);
        psnrMax = stod(argv[5]);
        psnrMin = stod(argv[6]);
        stepSize = stod(argv[7]);
        runType = argv[8];
        resumeFrame = atoi(argv[9]);
        extensionType = argv[10];
        
    }

    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frameCount: " << frameCount << endl;
    cout << "blockSize: " << blockSize << endl;
    cout << "tolerance: " << tolerance << endl;
    cout << "psnrMin: " << psnrMin << endl;
    cout << "psnrMax: " << psnrMax << endl;
    cout << "stepSize: " << stepSize << endl;
    cout << "runType: " << runType << endl;
    cout << "ResumeFrame (if valid): " << resumeFrame << endl;
    cout << "extensionType: " << extensionType << endl;
    
    if(runType == "n"){
        driverDifference(workspace,frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize, extensionType);
    }
    else if(runType == "r"){
        driverDifferenceResume(workspace,resumeFrame, frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize, extensionType);
    }
//    
    return 0;
}
