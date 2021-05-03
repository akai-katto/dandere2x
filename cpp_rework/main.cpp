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
#include "evaluator/SSIM_Function.h"
#include "plugins/block_plugins/block_matching/ExhaustiveSearch.h"
#include "plugins/block_plugins/block_matching/AbstractBlockMatch.h"
#include "driver.h"

using namespace std;

AbstractBlockMatch *get_block_matcher(const string &block_matcher_arg) {

    if (block_matcher_arg == "exhaustive")
        return new ExhaustiveSearch();

    throw std::logic_error("no valid block matcher selected");
}

AbstractEvaluator *get_evaluator(const string &evaluator_arg) {

    if (evaluator_arg == "mse")
        return new MSE_FUNCTIONS();

    if (evaluator_arg == "ssim")
        return new SSIM_Function();

    throw std::logic_error("no valid evaluator selected");
}

int main(int argc, char **argv) {
    bool debug = false; //debug flag

    string workspace = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace";
    string block_matching_arg = "exhaustive";
    string evaluator_arg = "mse";
    int frame_count = 720;
    int block_size = 20;

    cout << "Dandere2x CPP vDSSIM 1.0" << endl;
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
        block_matching_arg = argv[4];
    }

    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frame_count: " << frame_count << endl;
    cout << "block_size: " << block_size << endl;

    AbstractBlockMatch *matcher = get_block_matcher(block_matching_arg);
    AbstractEvaluator *evaluator = get_evaluator(evaluator_arg);
    driver_difference(workspace, frame_count, block_size, matcher, evaluator);

    free(matcher);
    return 0;
}