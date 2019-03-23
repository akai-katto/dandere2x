
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


//args = workspace, framecount, blockSize, tolerance, stepSize, 
int main(int argc, char** argv){
    
    bool debug = false; //debug flag
    
    string workspace = "C:\\Users\\windwoz\\Desktop\\workspace\\psnrtest\\";
    int frameCount = 144;
    int blockSize = 30;
    double tolerance = 15;
    double psnrMax = 95;
    double psnrMin = 85;
    int stepSize = 4;
    string runType = "n";// 'n' or 'r'
    int resumeFrame = 17;
    
    
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
    
    if(runType == "n"){
        driverDifference(workspace,frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize);
    }
    else if(runType == "r"){
        driverDifferenceResume(workspace,resumeFrame, frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize);
    }
//    
    return 0;
}
