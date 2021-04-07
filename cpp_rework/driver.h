//
// Created by tyler on 04/04/2021.
//

//utilities
char separator() {
#ifdef __CYGWIN__
    return '\\';
#else
    return '/';
#endif
}

#ifndef CPP_REWORK_DRIVER_H
#define CPP_REWORK_DRIVER_H

#include "plugins/predictive_frame/PredictiveFrame.h"

void driver_difference(string workspace,
                       int resume_count,
                       int frame_count,
                       int block_size) {
    auto *evaluation_library = new MSE_FUNCTIONS();

    // Input Files
    string image_prefix = workspace + separator() + "inputs" + separator() + "frame";

    // Output files
    string p_data_prefix = workspace + separator() + "pframe_data" + separator() + "pframe_";
    string residual_data_prefix = workspace + separator() + "residual_data" + separator() + "residual_";


    auto frame_1 = make_shared<Frame>(image_prefix + to_string(1) + ".png");
    for (int x = resume_count; x < frame_count; x++) {
        std::cout << "frame " << x << endl;

        // File Declarations
        string p_data_file = p_data_prefix + to_string(x) + ".txt";
        string residual_file = residual_data_prefix + to_string(x) + ".txt";

        // Load next frame files
        auto frame_2 = make_shared<Frame>(image_prefix + to_string(x + 1) + ".png");
        auto frame_2_compressed = make_shared<Frame>(image_prefix + to_string(x + 1) + ".png", 95);
        frame_2->apply_noise(8);
        frame_2_compressed->apply_noise(8);

        auto *search_library = new ExhaustiveSearch(*frame_2, *frame_1);

        PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library,
                                                          *frame_1, *frame_2, *frame_2_compressed, block_size);
        test_prediction.run();


        test_prediction.update_frame();
        test_prediction.write(p_data_file, p_data_prefix);
        frame_1 = frame_2;
    }

//    auto total_end = high_resolution_clock::now();
//    auto total_duration = duration_cast<microseconds>(total_end - total_start);
//    cout << "total time:  " << total_duration.count() << endl;

}

#endif //CPP_REWORK_DRIVER_H
