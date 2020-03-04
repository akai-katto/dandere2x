#include "Driver.h" //driver_difference
#include "Plugins/Fade/Fade.h"
#include "Image/DebugImage/DebugImage.h"



/*
 * It's a bit messy to leave this here, but this section is dedicated to doing random tests
 * On specific functions for Dandere2x. To use it, simply uncomment //benchmark() in the main class
 * to benchmark or test various features.
 */


void benchmark(){
#include "Image/Image.h"
#include "Plugins/PFrame/PFrame.h"

#include "BlockMatch/ExhaustiveSearch.h"
#include "Image/SSIM/SSIM.h"
#include "Image/SSIM/SsimStatsFunctions.h"

    Image im1 = Image("C:\\Users\\windwoz\\Desktop\\release\\workspace\\neg_test\\frame202.png");
    Image im2 = Image("C:\\Users\\windwoz\\Desktop\\release\\workspace\\neg_test\\frame203.png");

    double covariance = StatFunctions::covariance(im1, im2, 0, 0, 0,0, 60, 'g');
    double var = StatFunctions::variance_block(im1,  0, 0,  60, 'g');
    double mean = StatFunctions::mean_block(im1,  0, 0,  60, 'g');

    std::cout << "variance: " << var << std::endl;
    std::cout << "covariance: " << covariance << std::endl;
    std::cout << "mean: " << mean << std::endl;

    double ssim_r = SSIM::ssim(im1, im2, 0, 0, 0, 0, 60);
    std::cout << "ssim_r: " << ssim_r << std::endl;
}

int main(int argc, char **argv) {

//    cout << "hi" << endl;
//    benchmark();
////
    bool debug = false; //debug flag

    //Initialize the variables needed for Dandere2x's driver. If debug = True, then we use these variables.

    string workspace = "C:\\Users\\windwoz\\Desktop\\release\\workspace\\default\\";
    int frame_count = 205;
    int block_size = 30;
    int step_size = 8;
    string run_type = "r";// 'n' or 'r'
    int resume_frame = 200;
    string extension_type = ".jpg";

    cout << "Hello Dandere2!!" << endl;

    //load arguments
    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
        step_size = atoi(argv[4]);
        run_type = argv[5];
        resume_frame = atoi(argv[6]);
        extension_type = argv[7];
    }

    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frame_count: " << frame_count << endl;
    cout << "block_size: " << block_size << endl;
    cout << "step_size: " << step_size << endl;
    cout << "run_type: " << run_type << endl;
    cout << "ResumeFrame (if valid): " << resume_frame << endl;
    cout << "extension_type: " << extension_type << endl;

    if (run_type == "n")
        driver_difference(workspace, 1, frame_count, block_size, step_size, extension_type);
    else if (run_type == "r")
        driver_difference(workspace, resume_frame, frame_count, block_size, step_size, extension_type);

    return 0;
}
