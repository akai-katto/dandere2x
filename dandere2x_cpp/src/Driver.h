//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_DRIVER_H
#define DANDERE2X_DRIVER_H

#include "PFrame/Correction/Correction.h"
#include "PFrame/PFrame.h"
#include "Dandere2xUtils/Dandere2xUtils.h"
#include "Image/DebugImage/DebugImage.h"



/**
 * Todo:
 * - Simplify this driver class
 * - Add individual testing wrapper for debugging
 */


/**
 * Description:
 *
 * This is like the control room for Dandere2x - if you wish to add more additions to Dandere2x on the c++ side,
 * this where it is going to do it here.  Block matching, quality control, and saving of vectors all happen here.
 *
 *
 * Overview:
 *
 * - First we check if this is a resume frame, if it is, manually save the files as empty
 *   to create a p_frame at the resume frames position
 *
 *  //5-11-19  - this part is being overhauled - comments are outdated
 *
 */
using namespace dandere2x;
using namespace std;
const int correctionBlockSize = 5;


void driver_difference(string workspace, int resume_count, int frame_count,
                       int block_size,int step_size, string extension_type) {

    int bleed = 2; //i dont think bleed is actually used?

    wait_for_file(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + extension_type);
    shared_ptr<Image> im1 = make_shared<Image>(
            workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + extension_type);

    /** Handle Cases for Resuming Here*/

    if (resume_count != 1) {
        shared_ptr<Image> im2 = make_shared<Image>(
                workspace + separator() + "inputs" + separator() + "frame" + to_string(resume_count + 1) +
                extension_type);

        string p_data_file =
                workspace + separator() + "pframe_data" + separator() + "pframe_" + to_string(resume_count) + ".txt";

        string difference_file =
                workspace + separator() + "inversion_data" + separator() + "inversion_" + to_string(resume_count) +
                ".txt";

        string correction_file =
                workspace + separator() + "correction_data" + separator() + "correction_" + to_string(resume_count) +
                ".txt";

        write_empty(p_data_file);
        write_empty(difference_file);
        write_empty(correction_file);
        im1 = im2;

        resume_count++;
    }


    for (int x = resume_count; x < frame_count; x++) {
        cout << "\n\n Computing differences for frame" << x << endl;

        /** Locations of image files */
        string im2_file =
                workspace + separator() + "inputs" + separator() + "frame" + to_string(x + 1) + extension_type;

        string im2_file_compressed =
                workspace + separator() + "compressed" + separator() + "" + to_string(x + 1) + extension_type;

        shared_ptr<Image> im2 = make_shared<Image>(im2_file);
        shared_ptr<Image> im2_copy = make_shared<Image>(im2_file); //for corrections
        shared_ptr<Image> im2_compressed = make_shared<Image>(im2_file_compressed);

        //File locations that will be produced
        string p_data_file =
                workspace + separator() + "pframe_data" + separator() + "pframe_" + to_string(x) + ".txt";

        string inversion_file =
                workspace + separator() + "inversion_data" + separator() + "inversion_" + to_string(x) + ".txt";

        string correction_file =
                workspace + separator() + "correction_data" + separator() + "correction_" + to_string(x) + ".txt";

        /** Run dandere2xCpp Plugins (this is where all the computation of dandere2xcpp happens) */

        PFrame pframe = PFrame(im1, im2, im2_compressed, block_size, bleed, p_data_file, inversion_file, step_size);
        pframe.run();

        Correction correction = Correction(im2, im2_copy, im2_compressed, correctionBlockSize, correction_file, step_size);
        correction.run();

//        //For Debugging
//        DebugImage before = DebugImage::create_debug_from_image(*im2);
//        before.save(workspace + "debug_frames" + separator() + "before_" + to_string(x) + ".png");

        /** Save files if whatever plugins we ran through the image passed the quality test */

        pframe.save();
        correction.save();

        im1 = im2; //4
    }
}

#endif //DANDERE2X_DRIVER_H
