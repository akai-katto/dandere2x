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
#include "easyloggingpp/easylogging++.h"


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

INITIALIZE_EASYLOGGINGPP

int main(int argc, char **argv) {

    // Easy Logging Setup
    // Sample output: 2021-05-08 18:51:54,662 INFO main.cpp : block_size: 20
    el::Configurations c;
    c.setToDefault();
    c.parseFromText("*GLOBAL:\n Filename = default_log.txt");
    c.parseFromText("*GLOBAL:\n Format = %datetime %level %fbase : %msg");
    el::Loggers::reconfigureAllLoggers(c);

    // Parses the users inputs and starts the driver to preform Dandere2x Block Matching Calculations.
    bool debug = false; //debug flag

    string workspace = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace";
    string block_matching_arg = "exhaustive";
    string evaluator_arg = "mse";
    int frame_count = 240;
    int block_size = 20;
    int quality_setting = 100;
    int bleed = 1;

    // If not debug, load the passed variables.
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
        block_matching_arg = argv[4];
        evaluator_arg = argv[5];
        quality_setting = atoi(argv[6]);
        bleed = atoi(argv[7]);
    }
    // Reset log file now that args have been properly parsed.
    c.parseFromText("*GLOBAL:\n Filename = " + workspace + dandere2x_utilities::separator() + "dandere2x_cpp.log");
    el::Loggers::reconfigureAllLoggers(c);

    LOG(INFO) << "Dandere2xCPP 2021 v0.1";
    LOG(INFO) << "evaluator_arg: " << evaluator_arg << endl;
    LOG(INFO) << "block_matching_arg: " << block_matching_arg << endl;
    LOG(INFO) << "workspace: " << workspace << endl;
    LOG(INFO) << "frame_count: " << frame_count << endl;
    LOG(INFO) << "block_size: " << block_size << endl;
    LOG(INFO) << "quality setting: " << quality_setting << endl;

    // Start the main driver after having loaded the arguments
    AbstractBlockMatch *matcher = get_block_matcher(block_matching_arg);
    AbstractEvaluator *evaluator = get_evaluator(evaluator_arg);
    driver_difference(workspace, frame_count, block_size, quality_setting, bleed, matcher, evaluator);

    free(matcher); // Free used memory
    return 0;
}