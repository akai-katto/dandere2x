//
// Created by tylerpc on 9/14/2022.
//

#include "predictive_frame_dynamic_block_size.h"
#include "../predictive_frame/PredictiveFrame.h"
#include "../../easyloggingpp/easylogging++.h"

shared_ptr<PredictiveFrame> PredictiveFrameDynamicBlockSize::best_predictive_frame() {

    static int total_computations = 6;
    shared_ptr<PredictiveFrame> predictiveFrames[6] = {make_shared<PredictiveFrame>(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                10, this->bleed),
                                                       make_shared<PredictiveFrame>(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                20, this->bleed),
                                                       make_shared<PredictiveFrame>(this->eval,
                                                                this->block_matcher, this->current_frame,
                                                                this->next_frame, this->next_frame_compressed,
                                                                30, this->bleed),
                                                       make_shared<PredictiveFrame>(this->eval,
                                                                                    this->block_matcher, this->current_frame,
                                                                                    this->next_frame, this->next_frame_compressed,
                                                                                    40, this->bleed),
                                                       make_shared<PredictiveFrame>(this->eval,
                                                                                    this->block_matcher, this->current_frame,
                                                                                    this->next_frame, this->next_frame_compressed,
                                                                                    50, this->bleed),
                                                       make_shared<PredictiveFrame>(this->eval,
                                                                                    this->block_matcher, this->current_frame,
                                                                                    this->next_frame, this->next_frame_compressed,
                                                                                    60, this->bleed)};

    int lowest_index = 0;
    unsigned int lowest_index_value = 999999999;
    this->block_matcher->set_images(this->current_frame, this->next_frame);

        for (int i = 0; i < total_computations; i++){
            predictiveFrames[i]->run();
            LOG(INFO) << "blocksize: " << predictiveFrames[i]->get_block_size() << " " <<  predictiveFrames[i]->missing_pixel_cost() << endl;

            if (predictiveFrames[i]->missing_pixel_cost() < lowest_index_value){
                lowest_index = i;
                lowest_index_value = predictiveFrames[i]->missing_pixel_cost();
            }
    }

    LOG(INFO) << "lowest index is " << lowest_index << " with a value of " << lowest_index_value << endl;

    return predictiveFrames[lowest_index];
}
