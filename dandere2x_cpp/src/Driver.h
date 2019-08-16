//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_DRIVER_H
#define DANDERE2X_DRIVER_H

#include "Plugins/Correction/Correction.h"
#include "Plugins/PFrame/PFrame.h"
#include "Plugins/Fade/Fade.h"

#include "Dandere2xUtils/Dandere2xUtils.h"
#include "Image/DebugImage/DebugImage.h"



/**
 * Todo:
 * - Simplify this driver class
 */


/**
 * Description:
 *
 * This is like the control room for Dandere2x - if you wish to add more additions to Dandere2x on the c++ side,
 * this where it is going to do it here.  Block matching, quality control, and saving of vectors all happen here.
 */
using namespace dandere2x;
using namespace std;
const int correction_block_size = 2;

#include <chrono>
using namespace std::chrono;

void driver_difference(string workspace, int resume_count, int frame_count,
                       int block_size, int step_size, string extension_type)  {


    // Create pre-fixes for all the files needed to be accessed during dandere2x's runtime.
    // We do this primarly for readibility / maintability, as the files Dandere2x needs to
    // Interact with is very consistent in naming.

    string image_prefix = workspace + separator() + "inputs" + separator() + "frame";
    string p_data_prefix = workspace + separator() + "pframe_data" + separator() + "pframe_";
    string difference_prefix = workspace + separator() + "inversion_data" + separator() + "inversion_";
    string correction_prefix = workspace + separator() + "correction_data" + separator() + "correction_";
    string fade_prefix = workspace + separator() + "fade_data" + separator() + "fade_";
    string compressed_prefix = workspace + separator() + "compressed" + separator() + "compressed_";

   // DANDERE2x_CPP DRIVER STARTS HERE //

   // Before we start anything, we need to load the gensises image, image_1. This is because the first
   // Image is treated sort of differently in Dandere2x - it's the only image we can gurantee it is a 'i' frame,
   // And the entire image needs to be loaded.
    shared_ptr<Image> im1 = make_shared<Image>(image_prefix + to_string(1) + extension_type);

    // Dandere2x_cpp Handles the resume case by leaving everything empty, which serves as a signal to
    // Dandere2x_python simply draw a new frame at the resume frame.
    // Each plugin needs to have it's own 'resume' handling case.
    if (resume_count != 1) {

        shared_ptr<Image> im2 = make_shared<Image>(image_prefix + to_string(resume_count + 1) + extension_type);

        string p_data_file = p_data_prefix + to_string(resume_count) + ".txt";
        string difference_file = difference_prefix + to_string(resume_count) + ".txt";
        string correction_file = correction_prefix + to_string(resume_count) + ".txt";
        string fade_file = fade_prefix + to_string(resume_count) + ".txt";

        write_empty(p_data_file);
        write_empty(difference_file);
        write_empty(correction_file);
        write_empty(fade_file);

        im1 = im2;

        resume_count++;
    }

    auto total_start = high_resolution_clock::now();

    // Note that if Dandere2x is a new session, resume_count = 0.
    // Simply put, this for loop right here is pretty much the control room for 99% of the stuff
    // Happening within Dandere2x. The saving of files, the calculation of vectors, the loading of
    // Images all happens here.

    for (int x = resume_count; x < frame_count; x++) {
        auto frame_time_start = high_resolution_clock::now();
        cout << "\n\n Computing differences for frame: " << x << endl;

        // Create strings for the files we need to interact with for this computation iteration
        string im2_file = image_prefix + to_string(x + 1) + extension_type;
        string im2_file_compressed = compressed_prefix + to_string(x + 1) + ".jpg";

        // Wait for those files...
        dandere2x::wait_for_file(im2_file);
        dandere2x::wait_for_file(im2_file_compressed);

        // load actual images themselves
        shared_ptr<Image> im2 = make_shared<Image>(im2_file);
        shared_ptr<Image> im2_copy = make_shared<Image>(im2_file); //load im_2 twice for 'corrections'
        shared_ptr<Image> im2_compressed = make_shared<Image>(im2_file_compressed);

        // Create strings for the files we need to save for this computation iteration
        string p_data_file = p_data_prefix + to_string(x) + ".txt";
        string difference_file = difference_prefix + to_string(x) + ".txt";
        string correction_file = correction_prefix + to_string(x) + ".txt";
        string fade_file = fade_prefix + to_string(x) + ".txt";

        // First run the 'fade' plugin, which checks if two frames are simply fade to black / fade to white
        Fade fade = Fade(im1, im2, im2_compressed, block_size, fade_file);
        fade.run();

        // Find similar blocks between image_1 and image_2 for every block between im1 and im2.
        PFrame pframe = PFrame(im1, im2, im2_compressed, block_size, p_data_file, difference_file, step_size);
        pframe.run();

        // When finding similar blocks, there may be small blemishes left in as a result. Try our best
        // To find those errors, and replace them with nearby pixels. Use the original image as a reference
        // On how to preform these corrections.
        Correction correction = Correction(im2, im2_copy, im2_compressed, correction_block_size, correction_file, 2);
        correction.run();

        // Save the results for Dandere2x_python to use
        pframe.save();
        fade.save();
        correction.save();

       // For Debugging. Create a folder called 'debug_frames' in workspace when testing this -
       // Enabling this will allow you to see what Dandere2x_Cpp is seeing when it finishes processing a frame.
//        DebugImage before = DebugImage::create_debug_from_image(*im2);
//        before.save(workspace + "debug_frames" + separator() + "before_" + to_string(x) + ".png");


        // For the next iteration, we simply let frame 'x' become frame 'x+1'.
        // For example, when computing frame 100 -> 101, im1=100 and im2=101.
        // Assign im1=101, so when computing 101 -> 102, 101 is already loaded.
        im1 = im2;

        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - frame_time_start);
        cout << "Calculation time for frame :  " <<  duration.count() << endl;
    }

    auto total_end = high_resolution_clock::now();
    auto total_duration = duration_cast<microseconds>(total_end - total_start);

    cout << "total time:  " <<  total_duration.count() << endl;
}

#endif //DANDERE2X_DRIVER_H
