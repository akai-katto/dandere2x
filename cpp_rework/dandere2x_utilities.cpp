//
// Created by Tyler on 5/10/2021.
//
#include "dandere2x_utilities.h"
#include "easyloggingpp/easylogging++.h"
#include "math.h"

char dandere2x_utilities::separator() {
#ifdef __CYGWIN__
    return '\\';
#elif __GNUC__
    return '/';
#elif __MINGW64__
    return '\\';
#endif
}

bool dandere2x_utilities::file_exists(const std::string &name) {
    std::ifstream f(name.c_str());
    return f.good();
}

void dandere2x_utilities::wait_for_file(const std::string &name) {
    int count = 0;
    while (true) {
        if (file_exists(name))
            break;

// Need to call different sleep implementation depending on implementation.
#ifdef __MINGW64__
        Sleep(100);
#elif __GNUC__
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
#endif
        count++;
        if (std::remainder(count, 10) == 0) {
            LOG(WARNING) << "Waiting for file more than 1 sec: " << name << std::endl;
            count = 0;
        }
    }
}

bool dandere2x_utilities::debug_enabled() {
        return false;
}
