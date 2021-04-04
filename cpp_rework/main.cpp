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

using namespace std;


int main(){
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;


//    auto tempfile = make_shared<Frame>("C:\\Users\\Tyler\\Desktop\\releases\\3.1\\workspace\\gui\\subworkspace\\inputs\\frame139.jpg", 95);
//    tempfile->write("C:\\Users\\Tyler\\Desktop\\releases\\3.1\\workspace\\gui\\subworkspace\\pointer_test.jpg");


    auto *evaluation_library = new MSE_FUNCTIONS();
    string prefix = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\extracted\\frame";


    // pre loop setting variables
    int i = 1;
    auto frame_1 = make_shared<Frame>(prefix + to_string(i) + ".png");
    frame_1->apply_noise(8);

    // the actual loop
    for (; i < 51; i++) {

        std::cout << "frame " << i << endl;
        auto frame_2 = make_shared<Frame>(prefix + to_string(i+1) + ".png");
        auto frame_2_compressed = make_shared<Frame>(prefix + to_string(i+1) + ".png", 95);

        frame_2->apply_noise(8);
        frame_2_compressed->apply_noise(8);

        auto *search_library = new ExhaustiveSearch(*frame_2, *frame_1);

        cout << "hi 2" << endl;
        PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library,
                                                          *frame_1, *frame_2, *frame_2_compressed, 30);

        auto t1 = high_resolution_clock::now();
        test_prediction.run();
        auto t2 = high_resolution_clock::now();

        cout << "time: " << duration_cast<milliseconds>(t2 - t1).count() << endl;

        test_prediction.update_frame();
        test_prediction.write("C:\\Users\\Tyler\\Desktop\\scratch\\debug_frame\\frame" + to_string(i) + ".png",
                              "C:\\Users\\Tyler\\Desktop\\scratch\\debug_frame\\frame" + to_string(i) + ".txt");
//        test_prediction.debug_visual("C:\\Users\\Tyler\\Desktop\\scratch\\debug_frame_visual\\frame" + to_string(i) + ".png");
//        test_prediction.debug_predictive("C:\\Users\\Tyler\\Desktop\\scratch\\debug_frame_visual\\frame" + to_string(i) + ".png");
        frame_1 = frame_2;
    }

    return 0;
}