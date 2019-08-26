//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt


/**
 * Description:
 *
 * A recurring object that needs to be moved around in Dandere2x is something that holds the coordinates
 * of a block in one image, the coordinates of a block in another, and the MSE loss between the predicted block.
 */
#ifndef DANDERE2X_BLOCK_H
#define DANDERE2X_BLOCK_H

#include <iostream>

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

    Block(int x_start, int y_start, int x_end, int y_end, double sum) {
        this->x_start = x_start;
        this->y_start = y_start;
        this->x_end = x_end;
        this->y_end = y_end;
        this->sum = sum;
        this->valid = true;
    }

    Block() {
        this->x_start = -1;
        this->y_start = -1;
        this->x_end = -1;
        this->y_end = -1;
        this->sum = INT32_MAX;
        this->valid = false;
    }

    Block(const Block &other) {
        this->x_start = other.x_start;
        this->y_start = other.y_start;
        this->x_end = other.x_end;
        this->y_end = other.y_end;
        this->sum = other.sum;
        this->valid = other.valid;
    }

    bool operator<(const Block &other) {
        return this->sum < other.sum;
    }


    //for creating displacement vector files
    friend std::ostream &operator<<(std::ostream &os, Block &block) {
        return os << block.x_start << block.y_start << block.x_end << block.y_end << "\n";
    }

};


#endif //DANDERE2X_BLOCK_H
