#include "plugins/PredictiveFrame.h"
#include <chrono>
using namespace std::chrono;
#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION

#include <string>
#include <iostream>
#include <memory>
#include "frame/externals/stb_image_write.h"
#include "frame/externals/stb_image.h"
#include "frame/Frame.h"
#include <cstdio>
#include "evaluator/SSIM_Function.h"
#include "plugins/block_plugins/block_matching/ExhaustiveSearch.h"

using namespace std;


int main(){
    string file1_name = "/home/tyler/Downloads/yn_extracted/output1.png";
    string file2_name = "/home/tyler/Downloads/yn_extracted/output2.png";

    auto test = make_shared<Frame>(file1_name);
    auto test_2 = make_shared<Frame>(file2_name);
    auto test_2_compressed = make_shared<Frame>(file2_name, 99);

    auto *ssim = new SSIM_Function();
    auto *exhaustive_search = new ExhaustiveSearch(*test, *test);

    //cout << SSIM_Function::compute_ssim(test, test_compressed, 0,0,0,0,50);

    PredictiveFrame test_prediction = PredictiveFrame(ssim, exhaustive_search, test, test_2, test_2_compressed, 30);
    test_prediction.run();

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