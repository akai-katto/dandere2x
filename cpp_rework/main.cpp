#include "plugins/predictive_frame/PredictiveFrame.h"
#include <chrono>
using namespace std::chrono;
#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION

#include <string>
#include <iostream>
#include <memory>
#include "frame/Frame_Utilities.h"
#include "frame/external_headers/stb_image_write.h"
#include "frame/external_headers/stb_image.h"
#include "frame/Frame.h"
#include <cstdio>
#include "evaluator/SSIM_Function.h"
#include "evaluator/MSE_Function.h"
#include "plugins/block_plugins/block_matching/ExhaustiveSearch.h"
#include "driver.h"


using namespace std;


int main(int argc, char **argv) {
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    bool debug = false; //debug flag

    //Initialize the variables needed for Dandere2x's driver. If debug = True, then we use these variables.

    string workspace = "/home/tyler/Documents/workspace";
    int frame_count = 240;
    int block_size = 30;
    string run_type = "r";// 'n' or 'r'
    string extension_type = ".jpg";
    // cout << "Dandere2x CPP vDSSIM 1.0" << endl;

    //load arguments
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
    }
    driver_difference(workspace, 1, frame_count, block_size);

    return 0;
}