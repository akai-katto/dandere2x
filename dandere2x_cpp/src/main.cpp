
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
    
    string workspace;// = "/home/linux/Documents/workspace/work/";
    int frameCount;// = 144;
    int blockSize;// = 30;
    double tolerance;// = 15;
    int stepSize;// = 8;
    string runType; // 'n' or 'r'
    int resumeFrame; // 17
    
    if(!debug){
        workspace = argv[1];
        frameCount = stoi(argv[2]); 
        blockSize = atoi(argv[3]);
        tolerance = stod(argv[4]);
        stepSize = stod(argv[5]);
        runType = argv[6];
        resumeFrame = atoi(argv[7]);
    }

    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frameCount: " << frameCount << endl;
    cout << "blockSize: " << blockSize << endl;
    cout << "tolerance: " << tolerance << endl;
    cout << "stepSize: " << stepSize << endl;
    cout << "runType: " << runType << endl;
    cout << "ResumeFrame (if valid): " << resumeFrame << endl;
    
    if(runType == "n"){
        driverDifference(workspace,frameCount, blockSize, tolerance,stepSize);
    }
    else if(runType == "r"){
        driverDifferenceResume(workspace,resumeFrame, frameCount, blockSize, tolerance,stepSize);
    }
    
    return 0;
}
