#include "plugins/PredictiveFrame.h"
#include <chrono>
using namespace std::chrono;
#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION

#include <string>
#include <iostream>
#include <memory>
#include "frame/Frame_Utilities.h"
#include "frame/externals/stb_image_write.h"
#include "frame/externals/stb_image.h"
#include "frame/Frame.h"
#include <cstdio>
#include "evaluator/SSIM_Function.h"
#include "evaluator/MSE_Function.h"
#include "plugins/block_plugins/block_matching/ExhaustiveSearch.h"

using namespace std;


int main(){
    auto *evaluation_library = new MSE_FUNCTIONS();
    string prefix = "/home/tyler/Downloads/yn_extracted/output";

//    auto frame_1 = make_shared<Frame>(prefix + to_string(i) + ".png");
//    auto frame_1 = make_shared<Frame>(prefix + to_string(i) + ".png");



//    string prefix = "/home/tyler/Downloads/yn_extracted/output";
//
//    auto frame_1 = Frame("/home/tyler/Documents/test_scenario/" + to_string(1) + ".png");
//
//    //auto frame_1 = make_shared<Frame>("/home/tyler/Documents/test_scenario/" + to_string(100) + ".png");
//    //auto frame_2 = make_shared<Frame>("/home/tyler/Documents/test_scenario/" + to_string(2) + ".jpg");
//
//    frame_1.write("/home/tyler/Documents/test_scenario/test.png");
//    auto frame_2_compressed = make_shared<Frame>("/home/tyler/Documents/test_scenario/" + to_string(2) + ".jpg", 100);
//
//    auto *search_library = new ExhaustiveSearch(*frame_1, *frame_2);
//
//    PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library, *frame_1, *frame_2,
//                                                      *frame_2_compressed, 30);
//
//    test_prediction.run();
//    test_prediction.update_frame();
//    test_prediction.write("/home/tyler/Documents/test_scenario/frame_predicted.jpg");


    for (int i = 1; i < 51; i++) {

        auto frame_1 = make_shared<Frame>(prefix + to_string(i) + ".png");
        auto frame_2 = make_shared<Frame>(prefix + to_string(i+1) + ".png");
        auto frame_2_compressed = make_shared<Frame>(prefix + to_string(i+1) + ".png", 99);

        auto *search_library = new ExhaustiveSearch(*frame_2, *frame_1);

        PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library, *frame_1, *frame_2,
                                                          *frame_2_compressed, 30);

        test_prediction.run();
        test_prediction.update_frame();
        test_prediction.write("/home/tyler/Documents/debug_frames/frame" + to_string(i) + ".png");
    }

    return 0;
}