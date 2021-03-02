#define STB_IMAGE_WRITE_IMPLEMENTATION


#include <chrono>
using namespace std::chrono;

#include <string>
#include <iostream>
#include "frame/externals/stb_image_write.h"
#include "frame/externals/stb_image.h"
#include "frame/Frame.h"
#include <cstdio>

#include "evaluator/SSIM_Function.h"
using namespace std;


int main(){

    string file_name = "/home/tyler/Pictures/100.png";
    string name1 = std::tmpnam(nullptr);

    int width, height, bpp;
    unsigned char *stb_image = stbi_load(file_name.c_str(), &width, &height, &bpp, 3);

    auto start = high_resolution_clock::now();
    stbi_write_jpg(name1.c_str(), width, height, bpp, stb_image, 99);
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(stop - start);

// To get the value of duration use the count()
// member function on the duration object
    cout << duration.count() << endl;

    SSIM_Function ssim = SSIM_Function();
    cout << SSIM_Function::compute_ssim(Frame(file_name), Frame(name1), 0,0,0,0,50);

    return 0;
}