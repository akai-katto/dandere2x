//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_DANDERE2XUTILS_H
#define DANDERE2X_DANDERE2XUTILS_H

#include <string>
#include <iostream>
#include <fstream>

namespace dandere2x {

    char separator();

    inline bool file_exists(const std::string &name);

    void write_empty(std::string input);

    void wait_for_file(const std::string &name);

}

#endif //DANDERE2X_DANDERE2XUTILS_H
