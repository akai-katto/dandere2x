
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
Purpose: 
 
===================================================================== */


#include "DiamondSearch.h"
#include <algorithm>>

//-----------------------------------------------------------------------------
// Purpose: An iterative implementation of diamond search, plus or minus some
//          custom heuristics I've added myself.
//-----------------------------------------------------------------------------
Block DiamondSearch::match_block(int x, int y) {


    // These variables stay the same
    int x_bounds = desired_image.get_width();
    int y_bounds = desired_image.get_height();

    int x_origin = x;
    int y_origin = y;

    // These variables change per each iteration
    int initial_x = x;
    int initial_y = y;

    // Recycled variables that are cleared after each iteration
    std::vector<Block> blocks = std::vector<Block>();
    Block::Point point_array[CHECKS_PER_STEP];

    // Main loop .Note that if it hits the end of the for loop, we've gone over our max_checks, and this
    // are cutting the search short in order to keep the searching time having a constant worse-case search.
    // In other words, we're artificially capping the upper bounds.

    for (int x = 0; x < max_checks; x++) {

        // Base Cases (if we were doing this recursively, these essentially would be the base cases)
        {
            // If we ran out of checks, return what we're at right now
            if (x == max_checks - 1) {
                double sum = AbstractBlockMatch::mse_blocks(initial_x, initial_y, x_origin, y_origin);
                return Block(initial_x, initial_y, x_origin, y_origin, sum);
            }

            // If step size is 0, return where we are at right now, since we've reached the end of our search
            if (step_size <= 0) {
                double sum = AbstractBlockMatch::mse_blocks(initial_x, initial_y, x_origin, y_origin);
                return Block(initial_x, initial_y, x_origin, y_origin, sum);
            }
        }

        // Reset variables unique for each iteration
        blocks.clear();
        bool flag_array[16] = {true};
        {
            point_array[0].x = x_origin + step_size;
            point_array[0].y = y_origin;

            point_array[1].x = x_origin + step_size / 2;
            point_array[1].y = y_origin + step_size / 2;

            point_array[2].x = x_origin;
            point_array[2].y = y_origin + step_size;

            point_array[3].x = x_origin - step_size / 2;
            point_array[3].y = y_origin + step_size / 2;

            point_array[4].x = x_origin - step_size;
            point_array[4].y = y_origin;

            point_array[5].x = x_origin + step_size / 2;
            point_array[5].y = y_origin - step_size / 2;

            point_array[6].x = x_origin + step_size;
            point_array[6].y = y_origin;

            point_array[7].x = x_origin;
            point_array[7].y = y_origin;

            point_array[8].x = x_origin + step_size * 2;
            point_array[8].y = y_origin;

            point_array[9].x = x_origin + step_size;
            point_array[9].y = y_origin + step_size;

            point_array[10].x = x_origin;
            point_array[10].y = y_origin + step_size * 2;

            point_array[11].x = x_origin - step_size;
            point_array[11].y = y_origin + step_size;

            point_array[12].x = x_origin - step_size * 2;
            point_array[12].y = y_origin;

            point_array[13].x = x_origin + step_size;
            point_array[13].y = y_origin - step_size;

            point_array[14].x = x_origin + step_size * 2;
            point_array[14].y = y_origin;

            point_array[15].x = x_origin - step_size;
            point_array[15].y = y_origin - step_size;
        }


        // Create an array that is used to signal if a point is "valid" or not, i.e if it is legal to probe.
        bool any_legal_points = flag_invalid_points(x_bounds, y_bounds, point_array, CHECKS_PER_STEP, block_size,
                                                    flag_array);

        // Cycle through each search point (if it's legal that is) and add it to the block vector.
        for (int j = 0; j < CHECKS_PER_STEP; j++) {
            if (!flag_array[j]) { // checks if point is legal
                double sum = AbstractBlockMatch::mse_blocks(initial_x, initial_y, point_array[j].x, point_array[j].y);

                Block block = Block(initial_x, initial_y, point_array[j].x, point_array[j].y, sum);
                blocks.push_back(block);
            }
        }

        // Get the most promising block from the list (i.e the block with the smallest 'sum')
        std::vector<Block>::iterator smallest_block = min_element(blocks.begin(), blocks.end());

        // Custom-Implemented Heuristics #todo
        {
//            /** If the smallest block we found meets the MSE requirements, stop here*/
//            if (smallest_block->sum <= min_mse) {
//                return *smallest_block;
//            }
//
//
//            /** Testing feature - if the smallest block is garishly larger than the minimum required,
//             stop looking. */
//            if (smallest_block->sum >= min_mse * min_mse) {
//                return Block(0, 0, 0, 0, 10000);
//            }
        }


        // Assignments for next iteration

        if ((smallest_block->x_end == x_origin) && smallest_block->y_end == y_origin) {
            x_origin = smallest_block->x_end;
            y_origin = smallest_block->y_end;
            step_size /= 2;
            continue;
        } else {
            x_origin = smallest_block->x_end;
            y_origin = smallest_block->y_end;
        }

    }

    return Block();
}

void DiamondSearch::set_max_checks(int max_checks) {
    this->max_checks = max_checks;
}

void DiamondSearch::set_step_size(int step_size) {
    this->step_size = step_size;
}

//-----------------------------------------------------------------------------
// Purpose: Neatly construct all the points diamond search for probe.
//-----------------------------------------------------------------------------
Block::Point *DiamondSearch::get_diamond_search_points(int x_origin, int y_origin, int step_size) {

    //create the points to be used in diamond searching
    Block::Point point_array[CHECKS_PER_STEP];

    //construct the list of "diamond" points to be checked if legal or not
    point_array[0].x = x_origin + step_size;
    point_array[0].y = y_origin;

    point_array[1].x = x_origin + step_size / 2;
    point_array[1].y = y_origin + step_size / 2;

    point_array[2].x = x_origin;
    point_array[2].y = y_origin + step_size;

    point_array[3].x = x_origin - step_size / 2;
    point_array[3].y = y_origin + step_size / 2;

    point_array[4].x = x_origin - step_size;
    point_array[4].y = y_origin;

    point_array[5].x = x_origin + step_size / 2;
    point_array[5].y = y_origin - step_size / 2;

    point_array[6].x = x_origin + step_size;
    point_array[6].y = y_origin;

    point_array[7].x = x_origin;
    point_array[7].y = y_origin;

    point_array[8].x = x_origin + step_size * 2;
    point_array[8].y = y_origin;

    point_array[9].x = x_origin + step_size;
    point_array[9].y = y_origin + step_size;

    point_array[10].x = x_origin;
    point_array[10].y = y_origin + step_size * 2;

    point_array[11].x = x_origin - step_size;
    point_array[11].y = y_origin + step_size;

    point_array[12].x = x_origin - step_size * 2;
    point_array[12].y = y_origin;

    point_array[13].x = x_origin + step_size;
    point_array[13].y = y_origin - step_size;

    point_array[14].x = x_origin + step_size * 2;
    point_array[14].y = y_origin;

    point_array[15].x = x_origin - step_size;
    point_array[15].y = y_origin - step_size;

    return point_array;
}

bool DiamondSearch::flag_invalid_points(int x_bounds, int y_bounds, Block::Point *points, int size, int block_size,
                                        bool *flagged) {
    int count = 0;
    for (int i = 0; i < size; i++) {
        if ((points[i].x + block_size > x_bounds) || (points[i].x < 0) ||
            (points[i].y + block_size > y_bounds) || (points[i].y < 0)) {
            flagged[i] = true;
            count++;
        }
    }

    return count != size;
}
