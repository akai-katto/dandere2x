//
// Created by Tyler on 4/26/2021.
//

#ifndef CPP_REWORK_FADEFRAME_H
#define CPP_REWORK_FADEFRAME_H


#include <memory>
#include <utility>
#include "../AbstractPlugin.h"
#include "../../frame/Frame.h"
#include "../block_plugins/Block.h"
#include "../../evaluator/AbstractEvaluator.h"
#include "../block_plugins/block_matching/AbstractBlockMatch.h"

using namespace std;

class FadeFrame : public AbstractPlugin {
public:
    FadeFrame(AbstractEvaluator *eval,
              shared_ptr<Frame> current_frame,
              shared_ptr<Frame> next_frame,
              shared_ptr<Frame> next_frame_compressed,
              const int block_size) : AbstractPlugin(current_frame,
                                                     next_frame,
                                                     next_frame_compressed,
                                                     block_size) {
        current_frame_copy = shared_ptr<Frame>(current_frame);
        this->eval = eval;
    }

    void run() override;

    void update_frame(shared_ptr<Frame> final_frame) override;

    void write(const string &fade_file);

    int fade_block_count(){
        return this->fade_blocks.size();
    }

private:

    // Struct for holding vectors
    struct FadeBlock {
        int x;
        int y;
        double scalar;
    };

    int get_scalar_for_block(int x, int y);  // Finds a potential scalar for a block

    void parallel_function_call(int x, int y) override;

    static Frame::Color add_scalar_to_color(Frame::Color other_color, int scalar);

    static void add_scalar_to_image(const shared_ptr<Frame>& updated_frame, int x_start, int y_start, int scalar, int block_size);

    shared_ptr<Frame> current_frame_copy;
    AbstractEvaluator *eval;
    vector<FadeBlock> fade_blocks;
};

#endif //CPP_REWORK_FADEFRAME_H
