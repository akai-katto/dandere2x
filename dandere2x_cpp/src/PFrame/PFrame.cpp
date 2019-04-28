//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "PFrame.h"


PFrame::PFrame(std::shared_ptr<Image> image1, std::shared_ptr<Image> image2, unsigned int block_size, int bleed,
               double tolerance, std::string p_frame_file, std::string difference_file, int step_size, bool debug) {
    this->image1 = image1;
    this->image2 = image2;
    this->step_size = step_size;
    this->max_checks = 128; //prevent diamond search from going on forever
    this->block_size = block_size;
    this->width = image1->width;
    this->height = image1->height;
    this->dif = nullptr;
    this->p_frame_file = p_frame_file;
    this->difference_file = difference_file;
    this->bleed = bleed;
    this->tolerance = tolerance;
    this->debug = true;


    //Sanity Checks
    if (image1->height != image2->height || image1->width != image2->width)
        throw std::invalid_argument("PDifference image resolution does not match!");
}


/**
 * Run will modify image2 when the draw over command is called.
 */
void PFrame::run() {
    double psnr = ImageUtils::psnr(*image1, *image2);

    //if the psnr is really low between two images, don't bother trying to match blocks, as they're
    //probably wont be anyways to match
    if (psnr < 60) {
        std::cout << "PSNR is low - not going to match blocks" << std::endl;
        blocks.clear();
    }
        //if the PSNR is acceptable, try matching all the blocks.
    else {
        match_all_blocks();

        //if the amount of blocks matched is greater than 85% of the total blocks, throw away all the blocks.
        //At a certain point it's just easier / faster to redraw a scene rather than trying to piece
        //it back together.
        int max_blocks_possible = (this->height * this->width) / (this->block_size * this->block_size);
        if ((max_blocks_possible - blocks.size()) > (.85) * max_blocks_possible) {
            std::cout << "Too many missing blocks - conducting redraw" << std::endl;
            blocks.clear();
        }
    }

    draw_over();

}


/**
 * Saves the blocks (if they are there) into a relevent text files
 */
void PFrame::save() {
    if (!blocks.empty()) { //if parts of frame2 can be made of frame1, create frame2'
        create_difference();
        this->dif->write(difference_file);
        this->write(p_frame_file);
    } else { //if parts of frame2 cannot be made from frame1, just copy frame2.
        dandere2x::write_empty(difference_file);
        dandere2x::write_empty(p_frame_file);
    }
}


void PFrame::create_difference() {
    dif = std::make_shared<Differences>(blocks, block_size, bleed, image2);
    dif->run();
}

/**
 * Modifies image2 to carry the modifications given by the p_frame
 */
void PFrame::draw_over() {
    for (int outer = 0; outer < blocks.size(); outer++) {
        for (int x = 0; x < block_size; x++) {
            for (int y = 0; y < block_size; y++) {
                image2->set_color(x + blocks[outer].x_start,
                                  y + blocks[outer].y_start,
                                  image1->get_color(
                                          x + blocks[outer].x_end,
                                          y + blocks[outer].y_end));
            }
        }
    }
}

void PFrame::force_copy() {
    dandere2x::write_empty(difference_file);
    dandere2x::write_empty(p_frame_file);
}

void PFrame::match_all_blocks() {
    for (int x = 0; x < width / block_size; x++) {
        for (int y = 0; y < height / block_size; y++) {
            match_block(x, y);
        }
    }
}

void PFrame::match_block(int x, int y) {
    //initial disp is currently deprecated, but has ambitiouns to be introduced later.
    DiamondSearch::Point disp;
    disp.x = 0;
    disp.y = 0;

    double sum = ImageUtils::mse(
            *image1,
            *image2,
            x * block_size,
            y * block_size,
            x * block_size + disp.x,
            y * block_size + disp.y,
            block_size);

    //first we check if the blocks are in identical positions inbetween two frames.
    //if they are, we can skip doing a diamond search
    if (sum < tolerance) {
        blocks.push_back(Block(x * block_size,
                               y * block_size,
                               x * block_size + disp.x,
                               y * block_size + disp.y, sum));
    }//if the blocks have been (potentially) displaced, conduct a diamond search to search for them.
    else {
        //if it is lower, try running a diamond search around that area. If it's low enough add it as a displacement block.
        Block result =
                DiamondSearch::diamond_search_iterative_super(
                        *image2,
                        *image1,
                        x * block_size + disp.x,
                        y * block_size,
                        x * block_size + disp.x,
                        y * block_size + disp.y,
                        block_size,
                        step_size,
                        max_checks);

        //if the found block is lower than the required PSNR, we add it. Else, do nothing
        if (result.sum < tolerance)
            blocks.push_back(result);
    }
}

void PFrame::write(std::string output_file) {

    std::ofstream out(output_file + ".temp");
    for (int x = 0; x < blocks.size(); x++) {
        out <<
            blocks[x].x_start << "\n" <<
            blocks[x].y_start << "\n" <<
            blocks[x].x_end << "\n" <<
            blocks[x].y_end << std::endl;
    }
    out.close();

    rename((output_file + ".temp").c_str(), output_file.c_str());


}
