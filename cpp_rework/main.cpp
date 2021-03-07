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
    string file1_name = "/home/tyler/Downloads/yn_extracted/output100.png";
    string file2_name = "/home/tyler/Downloads/yn_extracted/output101.png";

    auto test = make_shared<Frame>(file1_name);
    auto test_2 = make_shared<Frame>(file2_name);

    auto start = high_resolution_clock::now();

    auto test_2_compressed = make_shared<Frame>(file2_name, 100, true);
    test_2_compressed->write("/home/tyler/Documents/Random/frame2_compressed.png");

    cout << duration_cast<microseconds>(high_resolution_clock::now() - start).count() << endl;

    test_2->apply_noise(8);
    test_2_compressed->apply_noise(8);


    test_2_compressed->write("/home/tyler/Documents/Random/finished.png");
    auto *ssim = new SSIM_Function();
    auto *exhaustive_search = new ExhaustiveSearch(*test, *test_2);

    //cout << SSIM_Function::compute_ssim(test, test_compressed, 0,0,0,0,50);

    PredictiveFrame test_prediction = PredictiveFrame(ssim, exhaustive_search, test, test_2, test_2_compressed, 60);
    test_prediction.run();
    test_prediction.write("/home/tyler/Documents/Random/new_frame_101.png");


//    test->write("/home/tyler/Documents/Random/ah.png");
//
//    vector<Block> vector_blocks = vector<Block>();
//    vector_blocks.emplace_back(100,100,150,150, -1);
//
//    Frame new_frame = FrameUtilities::copy_frame_using_blocks(*test, vector_blocks, 30);
//    new_frame.write("/home/tyler/Documents/Random/written.png");

//    string file_name = "/home/tyler/Pictures/100.png";
//    string name1 = std::tmpnam(nullptr);
//
//    int width, height, bpp;
//    unsigned char *stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);
//
//    auto start = high_resolution_clock::now();
//    stbi_write_jpg(name1.c_str(), width, height, bpp, stb_image, 99);
//    auto stop = high_resolution_clock::now();
//
//    auto duration = duration_cast<microseconds>(stop - start);
//
//// To get the value of duration use the count()
//// member function on the duration object
//    cout << duration.count() << endl;
//
//    SSIM_Function ssim = SSIM_Function();
//    cout << SSIM_Function::compute_ssim(Frame(file_name), Frame(name1), 0,0,0,0,50);

    return 0;
}