//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "Correction.h"

Correction::Correction(std::shared_ptr<Image> image1_fake, std::shared_ptr<Image> image1_true, unsigned int block_size,
                       double tolerance, std::string correction_file, int step_size) {

    this->image1_fake = image1_fake;
    this->image1_true = image1_true;
    this->step_size = step_size;
    this->max_checks = 64; //prevent diamond search from going on forever
    this->block_size = block_size;
    this->width = image1_fake->width;
    this->height = image1_fake->height;
    this->correction_file = correction_file;
    this->tolerance = tolerance;

    //preform checks to ensure given information is valid
    if (image1_fake->height != image1_true->height || image1_fake->width != image1_true->width)
        throw std::invalid_argument("PDifference image resolution does not match!");

}

void Correction::run() {
    match_all_blocks();
    draw_over();
}

void Correction::save() {
    std::ofstream out(this->correction_file + ".temp");

    for (int x = 0; x < blocks.size(); x++) {
        out << blocks[x].x_start << "\n" <<
            blocks[x].y_start << "\n" <<
            blocks[x].x_end << "\n" <<
            blocks[x].y_end << std::endl;
    }
    out.close();
    std::rename((this->correction_file + ".temp").c_str(), this->correction_file.c_str());

}

void Correction::draw_over() {
    for (int outer = 0; outer < blocks.size(); outer++) {
        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                image1_fake->set_color(
                        x + blocks[outer].x_start,
                        y + blocks[outer].y_start,
                        image1_fake->get_color(x + blocks[outer].x_end,
                                          y + blocks[outer].y_end));
            }
        }
    }
}

void Correction::match_block(int x, int y) {
    double sum = ImageUtils::mse(*image1_fake, *image1_true, x * block_size, y * block_size,
                                 x * block_size, y * block_size, block_size);


    if (sum < tolerance) {
    } else {
        //std::cout << "Conducting a diamond search" << std::endl;
        //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
        Block result = DiamondSearch::diamond_search_iterative_super(
                *image1_true,
                *image1_fake,
                x * block_size,
                y * block_size,
                x * block_size,
                y * block_size,
                block_size,
                step_size,
                max_checks);

        //std::cout << "Tolerance: " << result.sum << std::endl;

        //if the found block is lower than the required PSNR, we add it. Else, do nothing
        if (result.sum < tolerance) {
            //std::cout << "matched block" << std::endl;
            blocks.push_back(result);
        }
    }
}

void Correction::match_all_blocks() {
    for (int x = 0; x < width / block_size; x++) {
        for (int y = 0; y < height / block_size; y++) {
            match_block(x, y);
        }
    }
}
