//
// Created by tyler on 04/04/2021.
//

//utilities
char separator() {
#ifdef __CYGWIN__
    return '\\';
#elif __MINGW32_
    return '\\';
#else
    return '\\';
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
    string debug_frame_prefix = workspace + separator() + "debug" + separator() + "debug_";

    string correction_prefix = workspace + separator() + "correction_data" + separator() + "correction_";
    string fade_prefix = workspace + separator() + "fade_data" + separator() + "fade_";

    auto frame_1 = make_shared<Frame>(image_prefix + to_string(1) + ".png");
    // frame_1->convert_to_lab();

    int noise = 4;
    // frame_1->apply_noise(noise);
    for (int x = resume_count; x < frame_count; x++) {
        std::cout << "frame " << x << endl;

        // File Declarations
        string p_data_file = p_data_prefix + to_string(x) + ".txt";
        string residual_file = residual_data_prefix + to_string(x) + ".txt";
        string correction_file = correction_prefix + to_string(x) + ".txt";
        string fade_file = fade_prefix + to_string(x) + ".txt";
        string debug_file = debug_frame_prefix + to_string(x) + ".png";

        // Load next frame files
        auto frame_2 = make_shared<Frame>(image_prefix + to_string(x + 1) + ".png");
        auto frame_2_compressed = make_shared<Frame>(image_prefix + to_string(x + 1) + ".png", 95);

//        frame_2->apply_noise(noise);
//        frame_2_compressed->apply_noise(noise);
        // frame_2->convert_to_lab();
        // frame_2_compressed->convert_to_lab();

        auto *search_library = new ExhaustiveSearch(*frame_2, *frame_1);

        PredictiveFrame test_prediction = PredictiveFrame(evaluation_library, search_library,
                                                          *frame_1, *frame_2, *frame_2_compressed, block_size);
        test_prediction.run();
        test_prediction.debug_predictive(debug_file);
        // test_prediction.update_frame();
        test_prediction.write(p_data_file, residual_file);

        test_prediction.write_empty_file(fade_file);
        test_prediction.write_empty_file(correction_file);

        frame_1 = frame_2;
    }

//    auto total_end = high_resolution_clock::now();
//    auto total_duration = duration_cast<microseconds>(total_end - total_start);
//    cout << "total time:  " << total_duration.count() << endl;

}

#endif //CPP_REWORK_DRIVER_H
