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
    auto *evaluation_library = new SSIM_Function();
    string prefix = "/home/tyler/Downloads/yn_extracted/output";



    for (int i = 1; i < 200; i++) {

        auto frame_1 = make_shared<Frame>(prefix + to_string(1) + ".png");
        auto frame_2 = make_shared<Frame>(prefix + to_string(i+1) + ".png");
        auto frame_2_compressed = make_shared<Frame>(prefix + to_string(i+1) + ".png", 99);

        frame_1->apply_noise(2);
        frame_2->apply_noise(2);

        auto *search_library = new ExhaustiveSearch(*frame_2, *frame_1);

        PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library, *frame_1, *frame_2,
                                                          *frame_2_compressed, 30);

        test_prediction.run();
        test_prediction.update_frame();
        test_prediction.write("/home/tyler/Documents/debug_frames/frame" + to_string(i) + ".png");
    }

    return 0;
}