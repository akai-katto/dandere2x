#include "Driver.h"


//Known bugs: needs to run of CygWin due to directories acting weirdly
int main(int argc, char** argv) {

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
        driver_difference(workspace, 1, frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize, extensionType);
    }
    else if(runType == "r"){
        driver_difference(workspace,resumeFrame, frameCount, blockSize, tolerance, psnrMax, psnrMin, stepSize, extensionType);
    }
    return 0;
}