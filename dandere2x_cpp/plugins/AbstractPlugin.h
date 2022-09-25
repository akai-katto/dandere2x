
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
Purpose: An abstract class describing inherited d2x_cpp classes.
 
===================================================================== */


#ifndef CPP_REWORK_ABSTRACTPLUGIN_H
#define CPP_REWORK_ABSTRACTPLUGIN_H

#include <string>
#include <utility>
#include <fstream>
#include <memory>
#include "../frame/Frame.h"
#include "block_plugins/Block.h"

using namespace std;

class AbstractPlugin {
public:

    // Note that "current_frame" is not const, and can be updated in the "update_frame" function, once the plugin
    // "updates" it.
    AbstractPlugin(shared_ptr<Frame> current_frame,
                   shared_ptr<Frame> next_frame,
                   shared_ptr<Frame> next_frame_compressed,
                   const int block_size) {

        this->current_frame = current_frame;
        this->next_frame = next_frame;
        this->next_frame_compressed = next_frame_compressed;
        this->block_size = block_size;
    }


    // Every plugin needs to be 'ran' to some extent.
    virtual void run() = 0;

    // Every plugin needs to affect the frame somehow after it's done it's processing on it.
    virtual void update_frame(shared_ptr<Frame> final_frame) = 0;

    // Writes blocks in a python / c++ safe manner (writes to a tempfile then renames to prevent python from
    // pre-maturely reading). Checks if the "sum" is less than zero for each block, which denotes
    void write_blocks(const string &output, const vector<vector<shared_ptr<Block>>> &blocks) {
        // Write the predictive vectors out

        string temp_file = output + ".temp";
        std::ofstream out(temp_file);
        out << block_size << endl;

        for (const vector<shared_ptr<Block>> &row: blocks) {
            for (const shared_ptr<Block> &block: row) {
                // todo fix this technical debt, see the issues in "Predictive Frame"
                if (block == nullptr)
                    continue;

                if (block->sum != -1) { // -1 denotes an invalid block.
                    out <<
                        block->x_start << "\n" <<
                        block->y_start << "\n" <<
                        block->x_end << "\n" <<
                        block->y_end
                        << std::endl;
                }
            }
        }
        out.close();
        std::rename((temp_file).c_str(), output.c_str());
    }

    void write_empty_file(const string &output) {
        string temp_file = output + ".temp";
        std::ofstream out(temp_file);
        out << get_block_size() << endl;
        out.close();
        std::rename((temp_file).c_str(), output.c_str());
    }

    int get_block_size(){
        return this->block_size;
    }

protected:

    // Every plugin *should* utilize some sort of parallel optimization, although it doesn't need t.
    virtual void parallel_function_call(int x, int y) = 0;

    shared_ptr<Frame> current_frame;
    shared_ptr<Frame> next_frame;
    shared_ptr<Frame> next_frame_compressed;
    int block_size;


};

#endif //CPP_REWORK_ABSTRACTPLUGIN_H
