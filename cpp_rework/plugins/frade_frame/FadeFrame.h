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

class FadeFrame : AbstractPlugin {
public:
    FadeFrame(AbstractEvaluator *eval,
              Frame &current_frame,
              Frame &next_frame,
              const Frame &next_frame_compressed,
              const int block_size) : AbstractPlugin(current_frame,
                                                     next_frame,
                                                     next_frame_compressed,
                                                     block_size) {
        current_frame_copy = Frame(current_frame);
        this->eval = eval;
    }

    void run() override;

    void update_frame() override;

    void write(const string &fade_file);

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

    static void add_scalar_to_image(Frame &updated_frame, int x_start, int y_start, int scalar, int block_size);

    Frame current_frame_copy;
    AbstractEvaluator *eval;
    vector<FadeBlock> fade_blocks;
};

#endif //CPP_REWORK_FADEFRAME_H
