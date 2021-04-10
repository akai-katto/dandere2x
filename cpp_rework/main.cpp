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

<<<<<<< HEAD
=======
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
>>>>>>> parent of d2a7bb0 (backing up work)

using namespace std;

<<<<<<< HEAD

int main(int argc, char **argv) {
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

    bool debug = true; //debug flag
=======
    test_2_compressed->write("/home/tyler/Documents/Random/finished.png");
    auto *ssim = new SSIM_Function();
    auto *exhaustive_search = new ExhaustiveSearch(*test, *test_2);

    //cout << SSIM_Function::compute_ssim(test, test_compressed, 0,0,0,0,50);

    PredictiveFrame test_prediction = PredictiveFrame(ssim, exhaustive_search, test, test_2, test_2_compressed, 60);
    test_prediction.run();
    test_prediction.write("/home/tyler/Documents/Random/new_frame_101.png");
>>>>>>> parent of d2a7bb0 (backing up work)

    //Initialize the variables needed for Dandere2x's driver. If debug = True, then we use these variables.

    string workspace = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace";
    int frame_count = 240;
    int block_size = 20;
    string run_type = "r";// 'n' or 'r'
    string extension_type = ".jpg";
    // cout << "Dandere2x CPP vDSSIM 1.0" << endl;

<<<<<<< HEAD
    //load arguments
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
    }
    driver_difference(workspace, 1, frame_count, block_size);
=======
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
>>>>>>> parent of d2a7bb0 (backing up work)

    return 0;
}