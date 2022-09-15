//
// Created by tylerpc on 9/14/2022.
//

#ifndef DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H
#define DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H


#include "../AbstractPlugin.h"
#include "../../evaluator/AbstractEvaluator.h"
#include "../block_plugins/block_matching/AbstractBlockMatch.h"
#include "../predictive_frame/PredictiveFrame.h"

class PredictiveFrameDynamicBlockSize {
public:
    PredictiveFrameDynamicBlockSize(AbstractEvaluator *eval,
                                    AbstractBlockMatch *block_matcher,
                                    shared_ptr<Frame> current_frame,
                                    shared_ptr<Frame> next_frame,
                                    shared_ptr<Frame> next_frame_compressed,
                                    const int bleed) {
        this->eval = eval;
        this->block_matcher = block_matcher;
        this->current_frame = current_frame;
        this->next_frame = next_frame;
        this->next_frame_compressed = next_frame_compressed;
        this->bleed = bleed;
    }

    shared_ptr<PredictiveFrame> best_predictive_frame();

private:
    AbstractEvaluator *eval;
    AbstractBlockMatch *block_matcher;
    shared_ptr<Frame> current_frame;
    shared_ptr<Frame> next_frame;
    shared_ptr<Frame> next_frame_compressed;
    int bleed;
};


#endif //DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H
