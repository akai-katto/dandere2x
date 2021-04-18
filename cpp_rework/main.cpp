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



struct lab{
    float l;
    float a;
    float b;
};

lab get_lab_from_rgb(const Frame::Color& col){
    float_t var_R = float_t(col.r) / 255;
    float_t var_G = float_t(col.g) / 255;
    float_t var_B = float_t(col.b) / 255;

    var_R = (var_R > 0.04045) ? std::pow((var_R + 0.055) / 1.055, 2.4)
                              : var_R / 12.92;
    var_G = (var_G > 0.04045) ? std::pow((var_G + 0.055) / 1.055, 2.4)
                              : var_G / 12.92;
    var_B = (var_B > 0.04045) ? std::pow((var_B + 0.055) / 1.055, 2.4)
                              : var_B / 12.92;

    var_R *= 100;
    var_G *= 100;
    var_B *= 100;

    lab result;
    result.l = var_R * float_t(0.4124) + var_G * float_t(0.3576) + var_B * float_t(0.1805);
    result.a = var_R * float_t(0.2126) + var_G * float_t(0.7152) + var_B * float_t(0.0722);
    result.b = var_R * float_t(0.0193) + var_G * float_t(0.1192) + var_B * float_t(0.9505);

    return result;
}


using namespace std;

int main(int argc, char **argv) {
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;

//    auto color1 = Frame::Color();
//    color1.r = 128;
//    color1.g = 200;
//    color1.b = 192;
//
//    auto color2 = Frame::Color();
//    color2.r = 128;
//    color2.g = 200;
//    color2.b = 192;
//
//    auto lab = get_lab_from_rgb(color1);
//
//    cout << lab.l << endl;
//    cout << lab.a << endl;
//    cout << lab.b << endl;


    bool debug = true; //debug flag

    string workspace = "C:\\Users\\Tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace";
    int frame_count = 720;
    int block_size = 30;
    string run_type = "r";// 'n' or 'r'
    string extension_type = ".jpg";
    // cout << "Dandere2x CPP vDSSIM 1.0" << endl;
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
    }
    driver_difference(workspace, 1, frame_count, block_size);

    return 0;
}