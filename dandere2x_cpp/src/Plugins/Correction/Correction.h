//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CORRECTION_H
#define DANDERE2X_CORRECTION_H

#include <memory>
#include <iostream>
#include <fstream>

#include "Image/Image.h"
#include "BlockMatch/DiamondSearch.h"
#include "Dandere2xUtils/Dandere2xUtils.h"

/**
 * This can be seen as a second order approximation given the restrictions
 * outlined in the Dandere2x research paper ( see Restrictions)
 *
 * Given the fake version of an image and the real version, try to fix the fake
 * version of the image by using nearby blocks to correct the 'blemishes'
 * produced by waifu2x.
 *
 * In the end, we should have a series of vectors to help correct the 'fake' image,
 * as well as drawing over the fake image with said corrections.
 *
 *
 * Runtime
 *
 * - Correct image1_fake with relation to image1_true, looking for nearby
 *   blocks to hide artifacts produced by Dandere2x
 *
 * Results
 *
 * - A series of vectors to correct image1_fake with itself
 * - Draw over image1_fake with said produced vectors
 *
 */
class Correction {

public:
    Correction(std::shared_ptr<Image> image1_predicted,
               std::shared_ptr<Image> image1_true,
               std::shared_ptr<Image> image1_compressed,
               unsigned int block_size,
               std::string correction_file,
               int step_size);


    void run();

    void save();


private:
    int step_size;
    int max_checks;
    unsigned int block_size;
    int width;
    int height;
    std::string correction_file;

    std::vector<Block> blocks;
    std::shared_ptr<Image> image1_fake;
    std::shared_ptr<Image> image1_true;
    std::shared_ptr<Image> image1_compressed;

    void draw_over();

    void match_block(int x, int y);

    void match_all_blocks();

};


#endif //DANDERE2X_CORRECTION_H
