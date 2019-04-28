#include "Driver.h"

/**
 * Todo
 * - Implement CLI interface into dandere2x python for long -term usability.
 * - Debug function for people to test individual features
 */

/**
 * Known Bugs
 */
int main(int argc, char **argv) {
    bool debug = false; //debug flag

    string workspace = "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\";
    int frame_count = 2000;
    int block_size = 30;
    double tolerance = 15;
    double psnr_max = 4;
    double psnr_min = 2;
    int step_size = 4;
    string run_type = "n";// 'n' or 'r'
    int resume_frame = 23;
    string extension_type = ".jpg";

    if (!debug) {
        workspace = argv[1];
        frame_count = atoi(argv[2]);
        block_size = atoi(argv[3]);
        tolerance = stod(argv[4]);
        psnr_max = stod(argv[5]);
        psnr_min = stod(argv[6]);
        step_size = stod(argv[7]);
        run_type = argv[8];
        resume_frame = atoi(argv[9]);
        extension_type = argv[10];

    }

    cout << "Settings" << endl;
    cout << "workspace: " << workspace << endl;
    cout << "frame_count: " << frame_count << endl;
    cout << "block_size: " << block_size << endl;
    cout << "tolerance: " << tolerance << endl;
    cout << "psnr_min: " << psnr_min << endl;
    cout << "psnr_max: " << psnr_max << endl;
    cout << "step_size: " << step_size << endl;
    cout << "run_type: " << run_type << endl;
    cout << "ResumeFrame (if valid): " << resume_frame << endl;
    cout << "extension_type: " << extension_type << endl;

    if (run_type == "n") {
        driver_difference(workspace, 1, frame_count, block_size, tolerance, psnr_max, psnr_min, step_size,
                          extension_type);
    } else if (run_type == "r") {
        driver_difference(workspace, resume_frame, frame_count, block_size, tolerance, psnr_max, psnr_min, step_size,
                          extension_type);
    }


    return 0;
}
