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

#include "../BlockMatch/DiamondSearch.h"
#include "../Image/Image.h"
#include "../Dandere2xUtils/Dandere2xUtils.h"
#include "Difference/Differences.h"


class PFrame {

public:
    PFrame(std::shared_ptr<Image> image1, std::shared_ptr<Image> image2,
           unsigned int block_size, int bleed, double tolerance,
           std::string p_frame_file, std::string difference_file,
           int step_size = 5, bool debug = true);


    void run();

    void save();


private:
    int step_size;
    int max_checks;
    unsigned int block_size;
    int width;
    int height;
    unsigned int bleed;
    double tolerance;
    bool debug;

    std::string p_frame_file;
    std::string difference_file;

    std::vector<Block> blocks;
    std::shared_ptr<Image> image1;
    std::shared_ptr<Image> image2;
    std::shared_ptr<Differences> dif;

    void force_copy();

    void create_difference();

    void draw_over();

    void match_all_blocks();

    inline void match_block(int x, int y);

    void write(std::string output_file);


};


#endif //DANDERE2X_PFRAME_H
