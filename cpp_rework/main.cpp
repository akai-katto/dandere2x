#include "plugins/predictive_frame/PredictiveFrame.h"
#include <chrono>
using namespace std::chrono;
#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION

#include <string>
#include <iostream>
#include "frame/external_headers/stb_image_write.h"
#include "frame/external_headers/stb_image.h"
#include "evaluator/MSE_Function.h"
#include "plugins/block_plugins/block_matching/ExhaustiveSearch.h"
#include "driver.h"

using namespace std;

int main(int argc, char **argv) {
    bool debug = true; //debug flag

    string workspace = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace";
    int frame_count = 720;
    int block_size = 20;

    // cout << "Dandere2x CPP vDSSIM 1.0" << endl;
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
    }
    driver_difference(workspace, 1, frame_count, block_size);

    return 0;
}