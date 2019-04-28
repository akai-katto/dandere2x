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

#include "../../Image/Image.h"
#include "../../BlockMatch/DiamondSearch.h"
#include "../../Dandere2xUtils/Dandere2xUtils.h"

class Correction {

public:
    Correction(std::shared_ptr<Image> image1,
               std::shared_ptr<Image> image2,
               unsigned int block_size,
               double tolerance,
               std::string correction_file,
               int stepSize);


    void run();

    void save();


private:
    int step_size;
    int max_checks;
    unsigned int block_size;
    int width;
    int height;
    double tolerance;
    std::string correction_file;

    std::vector<Block> blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;

    void draw_over();

    void match_block(int x, int y);

    void match_all_blocks();

};


#endif //DANDERE2X_CORRECTION_H
