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

#include "../../Image/Image.h"
#include "../../BlockMatch/Block.h"
#include "DifferenceBlocks.h"


/*
 * Description:
 *
 *
 *
 * Comments:
 *
 * This is the closest thing to legacy code there is in my project. It's utterly confusing as shit to me
 * and I always have to re-read my own docs to understand what is going on here.
 *
 */


class Differences {
public:
    Differences(std::vector<Block> &blocks, int blockSize,
                int bleed, std::shared_ptr<Image> frame2) {
        this->blocks = blocks;
        this->block_size = blockSize;
        this->frame2 = frame2;
        this->bleed = bleed;
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
    int bleed;
    int height;
    int width;
    int blocks_needed;
    int dimensions;

    void flag_pixels();

    int count_empty_pixels();

    void add_missing_blocks_to_differences_blocks();
};


#endif //DANDERE2X_DIFFERENCES_H
