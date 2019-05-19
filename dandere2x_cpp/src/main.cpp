#include "Driver.h" //driver_difference

/**
 * Todo
 * - Implement CLI interface into dandere2x python for long -term usability.
 * - Debug function for people to test individual features.
 */


void benchmark(){
    #include "Image/Image.h"
    #include "PFrame/PFrame.h"

    Image f1 = Image("C:\\Users\\windwoz\\Desktop\\pythonreleases\\0.7\\demo_folder\\weeb\\inputs\\frame339.jpg");
    Image f2 = Image("C:\\Users\\windwoz\\Desktop\\pythonreleases\\0.7\\demo_folder\\weeb\\inputs\\frame340.jpg");

    std::cout << ImageUtils::mse(f1, f2, 50,50,50,50,30);


}

int main(int argc, char **argv) {
    //benchmark();

    bool debug = false; //debug flag

    string workspace = "C:\\Users\\windwoz\\Desktop\\workspace\\shelter_gradfun_higher_sens\\";
    int frame_count = 500;
    int block_size = 30;
    int step_size = 4;
    string run_type = "n";// 'n' or 'r'
    int resume_frame = 23;
    string extension_type = ".jpg";

    cout << "Hello Dandere!!" << endl;


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
