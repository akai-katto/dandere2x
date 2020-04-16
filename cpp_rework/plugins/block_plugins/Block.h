
/*
    This file is part of the Dandere2x project.

    Dandere2x is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dandere2x is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
*/

/* 
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Date: 4/11/20 
Purpose: A data structure representing the movement of a square grid
         within an image and MSE loss between the actual block
         between two frames.
===================================================================== */


#ifndef CPP_REWORK_BLOCK_H
#define CPP_REWORK_BLOCK_H

#include <iostream>
#include <limits>

class Block {
public:

    struct Point {
        int x;
        int y;
    };

    int x_start;
    int y_start;
    int x_end;
    int y_end;
    double sum;
    bool valid;

    Block(int x_start, int y_start, int x_end, int y_end, double sum);

    Block();

    Block(const Block &other);

    void flip_direction();

    string get_coordinate_string() const {
        return to_string(x_start) + " " + to_string(y_start) + " " +
               to_string(x_end) + " " + to_string(y_end);
    };

    // Overrides//

    // Compare a blocks mean squared error with relation to another block.
    bool operator<(const Block &other) {
        return this->sum < other.sum;
    }

    friend std::ostream &operator<<(std::ostream &os, Block &block) {
        return os << block.x_start << block.y_start << block.x_end << block.y_end << "\n";
    }


};

//---------------------------------------------------------------
// Purpose: Flip the direction a block goes (used in memoization)
//---------------------------------------------------------------
void Block::flip_direction() {
    int temp_x_start = x_start;
    int temp_y_start = y_start;

    x_start = x_end;
    y_start = y_end;
    x_end = temp_x_start;
    y_end = temp_y_start;
}

Block::Block(const Block &other) {
    this->x_start = other.x_start;
    this->y_start = other.y_start;
    this->x_end = other.x_end;
    this->y_end = other.y_end;
    this->sum = other.sum;
    this->valid = other.valid;
}

Block::Block() {
    this->x_start = -1;
    this->y_start = -1;
    this->x_end = -1;
    this->y_end = -1;
    this->sum = INT32_MAX;
    this->valid = false;
}

Block::Block(int x_start, int y_start, int x_end, int y_end, double sum) {
    this->x_start = x_start;
    this->y_start = y_start;
    this->x_end = x_end;
    this->y_end = y_end;
    this->sum = sum;
    this->valid = true;
}

#endif //CPP_REWORK_BLOCK_H
