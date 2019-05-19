//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_DIFFERENCES_H
#define DANDERE2X_DIFFERENCES_H


#include <memory> //smart pointers
#include <vector>

#include <iostream> //writing / reading
#include <fstream>

#include "Image/Image.h"
#include "BlockMatch/Block.h"
#include "DifferenceBlocks.h"


/**
 * Description:
 *
 * We know what blocks did get recycled between two frames, but we need to identify what blocks could not
 * be recycled in order to re-draw these parts for waifu2x
 *
 *
 * Inputs:
 *
 * 1) std::vector<Block> &blocks
 *
 *   All the blocks in this 'blocks' are 'accepted blocks' produced by block matching.
 *   Since we know what blocks DID get accepted, we need to find what blocks didn't.
 *
 * Runtime:
 *
 * - We need to know what pixels in the output image are empty, and we do this by flagging all the pixels
 *   that are covered because of blocks
 *
 * - We need to know how many pixels are missing in order to create the output image
 *
 * - Pixel by pixel, if a pixel is not marked as 'drawn' by a block, we need to add the block
 *   we're currently observing into the 'Difference Blocks' Object
 *
 *
 * Outcome:
 *
 * - A series of vectors that denote what parts of image2 could not be created using parts of image1
 *
 *
 * Comments:
 *
 * - This is the closest thing to legacy code there is in my project. It's utterly confusing as shit to me
 *   and I always have to re-read my own docs to understand what is going on here.
 *
 */


class Differences {
public:
    Differences(std::vector<Block> &blocks, int block_size, std::shared_ptr<Image> frame2) {
        this->blocks = blocks;
        this->block_size = block_size;
        this->frame2 = frame2;
        this->height = frame2->height;
        this->width = frame2->width;
    }

    void run();

    void write(std::string output_file);

private:

    std::vector<std::vector<bool>> occupied_pixel;
    std::vector<Block> blocks;
    std::shared_ptr<DifferenceBlocks> difference_blocks;
    std::shared_ptr<Image> frame2;

    int block_size;
    int height;
    int width;
    int dimensions;

    void flag_pixels();

    int count_empty_pixels();

    void add_missing_blocks_to_differences_blocks();
};


#endif //DANDERE2X_DIFFERENCES_H
