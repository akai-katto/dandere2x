//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_PFRAME_H
#define DANDERE2X_PFRAME_H

#include <memory>
#include <iostream>
#include <fstream>

#include "BlockMatch/DiamondSearch.h"
#include "Image/Image.h"
#include "Dandere2xUtils/Dandere2xUtils.h"
#include "Difference/Differences.h"


/**
 * Description:
 *
 * This is where the magic happens boy. This is honestly the core of Dandere2x -
 * we're given two images, and we try our best to create the second image using parts of the first
 * image. We document the parts that we could not reproduce ('Differences')  to be upscaled by
 * waifu2x, while everything else is recycled
 *
 *
 * Inputs:
 *
 * - image1 is the image we're trying to recycle parts from
 *
 * - image2 is the desired image we're trying to achieve
 *
 * Runtime:
 *
 * - If image1 and image2 are similiar enough, (we do this with a basic PSNR check),
 *   we try to identify where the blocks move in image1 to create image2
 *
 * - Once we know that image2 can be created from pieces of image1, we draw over those pieces
 *   into image2, creating a new image (that is noiser image) than true image2.
 *
 * Outputs:
 *
 * - A series of vectors to create image2 out of pieces using image1
 *
 * - Draw over image2 using pieces found in image1
 *
 * - A series of vectors to denote the parts of image2 that could not be drawn
 *   using parts of image1, so Waifu2x can re-upscale those parts
 *
 *
 */

class PFrame {

public:
    PFrame(std::shared_ptr<Image> image1, std::shared_ptr<Image> image2, std::shared_ptr<Image> image2_compressed,
           unsigned int block_size, std::string p_frame_file, std::string difference_file, int step_size = 4);

    void run();

    void save();

private:
    int step_size;
    int max_checks;
    unsigned int block_size;
    int width;
    int height;
    int count;

    std::string p_frame_file;
    std::string difference_file;

    std::vector<Block> blocks;

    std::vector<std::vector<Block>> matched_blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    std::shared_ptr<Image> image2_compressed;
    std::shared_ptr<Differences> dif;

    void force_copy();

    void create_difference();

    void draw_over();

    void match_all_blocks();

    inline void match_block(int x, int y);

    void write(std::string output_file);

};


#endif //DANDERE2X_PFRAME_H
