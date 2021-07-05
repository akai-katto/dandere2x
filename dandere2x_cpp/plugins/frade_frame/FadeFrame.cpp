//
// Created by Tyler on 4/26/2021.
//

#include "FadeFrame.h"
#include <cmath>

// todo, implement parralizable implementation for fade (if needed)
void FadeFrame::run() {
    for (int x = 0; x < current_frame->get_width() / block_size; x++) {
        for (int y = 0; y < current_frame->get_height() / block_size; y++) {
            parallel_function_call(x * block_size, y * block_size);
        }
    }
    update_frame();
}

void FadeFrame::update_frame() {

    for (auto fb : this->fade_blocks) {
        FadeFrame::add_scalar_to_image(current_frame, fb.x, fb.y, fb.scalar, block_size);
    }

}

void FadeFrame::write(const string &fade_file) {
    std::ofstream out(fade_file + ".temp");

    for (auto &fade_block : fade_blocks) {
        out <<
            fade_block.x << "\n" <<
            fade_block.y << "\n" <<
            fade_block.scalar <<
            std::endl;
    }

    out.close();
    std::rename((fade_file + ".temp").c_str(), fade_file.c_str());
}

// todo, comment
void FadeFrame::parallel_function_call(int x, int y) {
    int scalar = get_scalar_for_block(x, y);
    if (scalar == 0)
        return;

    FadeFrame::add_scalar_to_image(current_frame_copy, x, y, scalar, block_size);
    if (eval->evaluate(*this->current_frame_copy,
                       *this->next_frame, *this->next_frame_compressed,
                       x, y,
                       x, y,
                       block_size)) {
        FadeBlock current_fade{};

        current_fade.scalar = scalar;
        current_fade.x = x;
        current_fade.y = y;

        fade_blocks.push_back(current_fade);
    }
}

int FadeFrame::get_scalar_for_block(int x, int y) {
    double sum = 0;

    for (int i = x; i < x + block_size; i++) {
        for (int j = y; j < y + block_size; j++) {

            Frame::Color col1 = current_frame->get_color(i, j);
            Frame::Color col2 = next_frame->get_color(i, j);

            sum += (int) (col2.r - col1.r) + (int) (col2.g - col1.g) + (int) (col2.b - col1.b);
        }
    }

    return (int) std::round((sum / ((block_size * block_size) * 3)));
}

//-----------------------------------------------------------------------------
// Purpose: Creates a new color by adding the flat scalar to the color.
//          Takes into account that the added color might push the color
//          out of bounds, in which case a floor / ceil function is applied.
//-----------------------------------------------------------------------------
Frame::Color FadeFrame::add_scalar_to_color(Frame::Color other_color, int scalar) {

    int r = (int) other_color.r + scalar;
    int g = (int) other_color.g + scalar;
    int b = (int) other_color.b + scalar;
    return Frame::bound_color(r, g, b);
}


void FadeFrame::add_scalar_to_image(const shared_ptr<Frame>& updated_frame, int x_start, int y_start, int scalar, int block_size) {
    for (int x = x_start; x < x_start + block_size; x++) {
        for (int y = y_start; y < y_start + block_size; y++) {
            Frame::Color col = add_scalar_to_color(updated_frame->get_color(x, y), scalar);
            updated_frame->set_color(x, y, col);
        }
    }
}

