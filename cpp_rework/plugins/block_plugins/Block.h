
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
#include <string>

using namespace std;

class Block {
    friend class BlockMatchingMemoization;

public:

    // A nifty struct to have when block matching.
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

    void flip_direction(); // used in optimization techniques (memoization)

    [[nodiscard]] bool is_equivalent(const Block &other) const;

    // Compare a blocks mean squared error with relation to another block.
    bool operator<(const Block &other) {
        return this->sum < other.sum;
    }

    friend std::ostream &operator<<(std::ostream &os, Block &block) {
        return os << block.x_start <<" " <<  block.y_start << " " << block.x_end << " " << block.y_end << "\n";
    }


// Ignore these sections unless you're working with memoization
protected:
    unsigned long left_to_right_hash;
    unsigned long right_to_left_hash;
};



#endif //CPP_REWORK_BLOCK_H
