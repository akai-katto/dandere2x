//
// Created by tyler on 04/04/2021.
//

#ifndef CPP_REWORK_DRIVER_H
#define CPP_REWORK_DRIVER_H

#include "dandere2x_utilities.h"

using namespace dandere2x_utilities;

#include "plugins/predictive_frame/PredictiveFrame.h"
#include "plugins/frade_frame/FadeFrame.h"
#include "plugins/block_plugins/block_matching/AbstractBlockMatch.h"
#include "easyloggingpp/easylogging++.h"

void driver_difference(const string &workspace,
                       const int frame_count,
                       const int block_size,
                       const int quality_setting,
                       const int bleed,
                       AbstractBlockMatch *search_library,
                       AbstractEvaluator *evaluation_library) {

    // Input Files
    string image_prefix = workspace + separator() + "noised_inputs" + separator() + "frame";

    // Output files
    string p_data_prefix = workspace + separator() + "pframe_data" + separator() + "pframe_";
    string residual_data_prefix = workspace + separator() + "residual_data" + separator() + "residual_";
    string debug_frame_prefix = workspace + separator() + "debug" + separator() + "debug_";
    string fade_prefix = workspace + separator() + "fade_data" + separator() + "fade_";

    auto frame1_path = image_prefix + to_string(1) + ".png";

    wait_for_file(frame1_path);
    auto frame_1 = make_shared<Frame>(frame1_path);

    for (int x = 1; x < frame_count; x++) {
        LOG(INFO) << "Current Frame: " << x << endl;

        // File Declarations
        string p_data_file = p_data_prefix + to_string(x) + ".txt";
        string residual_file = residual_data_prefix + to_string(x) + ".txt";
        string fade_file = fade_prefix + to_string(x) + ".txt";
        string debug_file = debug_frame_prefix + to_string(x) + ".png";

        // Load next frame files
        auto frame_2_path = image_prefix + to_string(x + 1) + ".png";
        wait_for_file(frame_2_path);

        auto frame_2 = make_shared<Frame>(frame_2_path);
        auto frame_2_compressed = make_shared<Frame>(frame_2_path, quality_setting, workspace);

        FadeFrame fade = FadeFrame(evaluation_library, frame_1, frame_2, frame_2_compressed, block_size);
        fade.run();
        fade.write(fade_file);

//        FadeFrame::write_empty_file(fade_file);

        search_library->set_images(frame_1, frame_2);
        PredictiveFrame predict = PredictiveFrame(evaluation_library, search_library,
                                                  frame_1, frame_2, frame_2_compressed, block_size, bleed);
        predict.run();
        predict.write(p_data_file, residual_file);

        if (debug_enabled()) {
            predict.debug_predictive(debug_file);
        }

        frame_1 = frame_2;
    }
}

#endif //CPP_REWORK_DRIVER_H
