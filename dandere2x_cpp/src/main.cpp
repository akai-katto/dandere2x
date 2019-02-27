
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


int main(int argc, char** argv){
    string workspace;// = "/home/linux/Videos/5cmrun/";
    int frameCount;// = 144;
    int blockSize;// = 30;
    double tolerance;// = 15;
    int stepSize;// = 8;


    if(argc==1){
        cout << " No arguments given " << endl;
        return 1;
    }

    if(argv[1] && argv[2]){
        cout << argv[1] << " " << argv[2] << endl;
        workspace = argv[1];
        frameCount = stoi(argv[2]);
    }

    if(argv[3] && argv[4] && argv[5]){
        cout << "using custom block size and tolerance" << endl;
        blockSize = atoi(argv[3]);
        tolerance = stod(argv[4]);
        stepSize = stod(argv[5]);
    }
    else{
        blockSize = 30;
        tolerance = 15;
    }


    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frameCount: " << frameCount << endl;
    cout << "blockSize: " << blockSize << endl;
    cout << "tolerance: " << tolerance << endl;
    cout << "stepSize: " << stepSize << endl;
    driverDifference(workspace,frameCount, blockSize, tolerance,stepSize);

    return 0;
}
