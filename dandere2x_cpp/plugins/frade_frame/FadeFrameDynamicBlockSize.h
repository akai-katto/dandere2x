//
// Created by Tyler Szeto on 9/17/22.
//

#ifndef DANDERE2X_CPP_FADEFRAMEDYNAMICBLOCKSIZE_H
#define DANDERE2X_CPP_FADEFRAMEDYNAMICBLOCKSIZE_H


#include "../AbstractPlugin.h"
#include "../../evaluator/AbstractEvaluator.h"
#include "../block_plugins/block_matching/AbstractBlockMatch.h"
#include "../../easyloggingpp/easylogging++.h"
#include "FadeFrame.h"


class FadeFrameDynamicBlockSize {
public:
    FadeFrameDynamicBlockSize(AbstractEvaluator *eval,
                                    AbstractBlockMatch *block_matcher,
                                    shared_ptr<Frame> current_frame,
                                    shared_ptr<Frame> next_frame,
                                    shared_ptr<Frame> next_frame_compressed) {
        this->eval = eval;
        this->block_matcher = block_matcher;
        this->current_frame = current_frame;
        this->next_frame = next_frame;
        this->next_frame_compressed = next_frame_compressed;
    }

    shared_ptr<FadeFrame> best_predictive_frame() {

        static int total_computations = 6;
        shared_ptr<FadeFrame> fade_frames[6] = {make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                       this->next_frame, this->next_frame_compressed,
                                                                       60),
                                                make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                                        this->next_frame, this->next_frame_compressed,
                                                                                        20),
                                                make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                                        this->next_frame, this->next_frame_compressed,
                                                                                        30),
                                                make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                                        this->next_frame, this->next_frame_compressed,
                                                                                        40),
                                                make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                                        this->next_frame, this->next_frame_compressed,
                                                                                        50),
                                                make_shared<FadeFrame>(this->eval, this->current_frame,
                                                                                        this->next_frame, this->next_frame_compressed,
                                                                                        10)};

        int highest_index = 0;
        unsigned int highest_index_value = 0;
        this->block_matcher->set_images(this->current_frame, this->next_frame);

        for (int i = 0; i < total_computations; i++){
            fade_frames[i]->run();
            LOG(INFO) << "blocksize: " << fade_frames[i]->get_block_size() << " " << fade_frames[i]->fade_block_count() << endl;

            if (fade_frames[i]->fade_block_count() > highest_index_value){
                highest_index = i;
                highest_index_value = fade_frames[i]->fade_block_count();
            }
        }

        LOG(INFO) << "lowest index is " << highest_index << " with a value of " << highest_index_value << endl;

        return fade_frames[highest_index];
    }


private:
    AbstractEvaluator *eval;
    AbstractBlockMatch *block_matcher;
    shared_ptr<Frame> current_frame;
    shared_ptr<Frame> next_frame;
    shared_ptr<Frame> next_frame_compressed;
    int bleed;
};

#endif //DANDERE2X_CPP_FADEFRAMEDYNAMICBLOCKSIZE_H
