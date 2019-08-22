//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#include "Dandere2xUtils.h"


char dandere2x::separator() {
#ifdef __MINGW__
    return '\\';
#else
    return '\\';
#endif
}

//credit to https://stackoverflow.com/questions/12774207/fastest-way-to-check-if-a-file-exist-using-standard-c-c11-c
//returns true if file exists, false if not.
bool dandere2x::file_exists(const std::string &name) {
    std::ifstream f(name.c_str());
    return f.good();
}


//write an empty text file
void dandere2x::write_empty(std::string input) {
    std::ofstream out(input);
    out.close();
}


//wait for a file to exist. Consider adding a time out / throw time if not,
//but for the time being this is a system agnostic function call.
void dandere2x::wait_for_file(const std::string &name) {
    int count = 0;
    while (!file_exists(name)) {
        if (count % 10000 == 0) {
            std::cout << "waiting for file " << name << std::endl;
            count = 0;
        }
        count++;
    }
}
