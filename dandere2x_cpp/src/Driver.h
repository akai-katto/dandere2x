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


using namespace dandere2x;
using namespace std;

const int correctionBlockSize = 4;



void driver_difference(string workspace, int resume_count, int frame_count, int block_size,
                       double tolerance, double mse_max, double mse_min, int step_size, string extension_type) {

    int bleed = 2; //i dont think bleed is actually used?
    bool debug = true;

    //1
    wait_for_file(workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + extension_type);
    shared_ptr<Image> im1 = make_shared<Image>(
            workspace + separator() + "inputs" + separator() + "frame" + to_string(1) + extension_type);


    //for resume case, we need to manually process this frame in a different manner.
    if (resume_count != 1) {

        shared_ptr<Image> im2 = make_shared<Image>(
                workspace + separator() + "inputs" + separator() + "frame" + to_string(resume_count + 1) +
                extension_type);

        //File locations that will be produced
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

        shared_ptr<Image> im2 = make_shared<Image>(
                workspace + separator() + "inputs" + separator() + "frame" + to_string(x + 1) + extension_type);
        shared_ptr<Image> copy = make_shared<Image>(
                workspace + separator() + "inputs" + separator() + "frame" + to_string(x + 1) +
                extension_type); //for psnr

        //File locations that will be produced
        string pDataFile = workspace + separator() + "pframe_data" + separator() + "pframe_" + to_string(x) + ".txt";
        string inversionFile =
                workspace + separator() + "inversion_data" + separator() + "inversion_" + to_string(x) + ".txt";
        string correctionFile1 =
                workspace + separator() + "correction_data" + separator() + "correction_" + to_string(x) + ".txt";

        PFrame p = PFrame(im1, im2, block_size, bleed, tolerance, pDataFile, inversionFile, step_size, debug);
        p.run();

        int correction_factor = sqrt(block_size) / sqrt(correctionBlockSize); // not rly sure why this works tbh

        Correction c = Correction(im2, copy, correctionBlockSize, tolerance * correction_factor, correctionFile1,
                                  correctionBlockSize);
        c.run();

        double p_mse = ImageUtils::mse_image(*im2, *copy);
        cout << "p_frame # " << x << "  mse: " << p_mse << endl;

        if (p_mse > mse_max && tolerance > 1) {
            cout << "mse too high " << p_mse << " > " << mse_max << endl;
            cout << "Changing Tolerance " << tolerance << " -> " << tolerance - 1 << endl;
            tolerance--;
            x--;
            continue; //redo this current for loop iteration with different settings
        }

        if (p_mse < mse_min && tolerance < 30 && p_mse != 0) {
            cout << "mse too too low: " << p_mse << " < " << mse_min << endl;
            cout << "Changing Tolerance " << tolerance << " -> " << tolerance + 1 << endl;
            tolerance++;
        }

        p.save();
        c.save();
        im1 = im2; //4
    }
}

#endif //DANDERE2X_DRIVER_H
