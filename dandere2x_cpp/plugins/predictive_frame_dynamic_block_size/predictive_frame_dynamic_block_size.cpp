//
// Created by tylerpc on 9/14/2022.
//

#include "predictive_frame_dynamic_block_size.h"
#include "../predictive_frame/PredictiveFrame.h"

shared_ptr<PredictiveFrame> PredictiveFrameDynamicBlockSize::best_predictive_frame() {

    int total_computations = 3;
    PredictiveFrame * predictiveFrames[3] = {new PredictiveFrame(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                15, this->bleed),
                                            new PredictiveFrame(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                30, this->bleed),
                                            new PredictiveFrame(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                50, this->bleed)};
    this->block_matcher->set_images(this->current_frame, this->next_frame);
    for (int i = 0; i < total_computations; i++){
            predictiveFrames[i]->run();
            cout << "blocksize: " << predictiveFrames[i]->get_block_size() << " " <<  predictiveFrames[i]->missing_pixel_cost() << endl;
    }

    return nullptr;
}
