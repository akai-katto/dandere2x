//
// Created by tylerpc on 9/14/2022.
//

#ifndef DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H
#define DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H


#include <utility>

#include "../AbstractPlugin.h"
#include "../../evaluator/AbstractEvaluator.h"
#include "../block_plugins/block_matching/AbstractBlockMatch.h"
#include "PredictiveFrame.h"
#include "../../easyloggingpp/easylogging++.h"
#include <thread>
#include <future>

using namespace std;

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
        this->current_frame = move(current_frame);
        this->next_frame = move(next_frame);
        this->next_frame_compressed = move(next_frame_compressed);
        this->bleed = bleed;
    }

    static void pframe_thread(AbstractEvaluator *eval,
                              AbstractBlockMatch *block_matcher,
                              const shared_ptr<const Frame> &current_frame,
                              const shared_ptr<const Frame> &next_frame,
                              const shared_ptr<const Frame> &next_frame_compressed,
                              const int block_size,
                              const int bleed,
                              promise<shared_ptr<PredictiveFrame>> *promObj) {
        shared_ptr<PredictiveFrame> predictiveFrame = make_shared<PredictiveFrame>(eval, block_matcher, current_frame,
                                                                                   next_frame, next_frame_compressed,
                                                                                   block_size, bleed);
        predictiveFrame->run();
        promObj->set_value(predictiveFrame);
    }


    shared_ptr<PredictiveFrame> best_predictive_frame() {

        static int total_computations = 4;
        int block_sizes[] = {10, 20, 30,60};
        promise<shared_ptr<PredictiveFrame>> promises[] = {promise<shared_ptr<PredictiveFrame>>(),
                                                           promise<shared_ptr<PredictiveFrame>>(),
                                                           promise<shared_ptr<PredictiveFrame>>(),
                                                           promise<shared_ptr<PredictiveFrame>>()};

        thread threads[] = {thread(pframe_thread, this->eval,
                                   this->block_matcher,
                                   this->current_frame,
                                   this->next_frame,
                                   this->next_frame_compressed,
                                   block_sizes[0], this->bleed, &promises[0]),
                            thread(pframe_thread, this->eval,
                                   this->block_matcher,
                                   this->current_frame,
                                   this->next_frame,
                                   this->next_frame_compressed,
                                   block_sizes[1], this->bleed, &promises[1]),
                            thread(pframe_thread, this->eval,
                                   this->block_matcher,
                                   this->current_frame,
                                   this->next_frame,
                                   this->next_frame_compressed,
                                   block_sizes[2], this->bleed, &promises[2]),
                            thread(pframe_thread, this->eval,
                                   this->block_matcher,
                                   this->current_frame,
                                   this->next_frame,
                                   this->next_frame_compressed,
                                   block_sizes[3], this->bleed, &promises[3])};

        for (int i = 0; i < total_computations; i++) {
            threads[i].join();
        }

        shared_ptr<PredictiveFrame> predictive_frames[] = {shared_ptr<PredictiveFrame>(),
                                                           shared_ptr<PredictiveFrame>(),
                                                           shared_ptr<PredictiveFrame>(),
                                                           shared_ptr<PredictiveFrame>()};

        int lowest_index = 0;
        unsigned int lowest_index_value = 999999999;
        this->block_matcher->set_images(this->current_frame, this->next_frame);

        for (int i = 0; i < total_computations; i++) {
            shared_ptr<PredictiveFrame> predictiveFrameFuture = promises[i].get_future().get();
            predictive_frames[i] = predictiveFrameFuture;
            LOG(INFO) << "blocksize: " << predictiveFrameFuture->get_block_size() << " "
                      << predictiveFrameFuture->missing_pixel_cost() << endl;

            if (predictiveFrameFuture->missing_pixel_cost() < lowest_index_value) {
                lowest_index = i;
                lowest_index_value = predictiveFrameFuture->missing_pixel_cost();
            }
        }

        LOG(INFO) << "lowest index is " << lowest_index << " with a value of " << lowest_index_value << endl;

        return predictive_frames[lowest_index];
    }


private:
    AbstractEvaluator *eval;
    AbstractBlockMatch *block_matcher;
    shared_ptr<Frame> current_frame;
    shared_ptr<Frame> next_frame;
    shared_ptr<Frame> next_frame_compressed;
    int bleed;
};


#endif //DANDERE2X_CPP_PREDICTIVE_FRAME_DYNAMIC_BLOCK_SIZE_H
