/*
 * Pretty dis-interesting function. Literally exists to call 
 * when we need to get a seperator character, as unix based systems
 * and windows use a different character
 */

#ifndef SEPERATOR_H
#define SEPERATOR_H

#include <string>

inline char separator()
{
#ifdef __CYGWIN__
    return '\\';
#else
    return '/';
#endif
}

//credit to https://stackoverflow.com/questions/12774207/fastest-way-to-check-if-a-file-exist-using-standard-c-c11-c



//returns true if file exists, false if not.
inline bool fileExists(const std::string& name) {
    ifstream f(name.c_str());
    return f.good();
}


//wait for a file to exist. Consider adding a time out / throw time if not, 
//but for the time being this is a system agnostic function call.
void waitForFile(const std::string& name){
    do{
    	std::cout << "waiting for file "<< name << endl;
    }while(!fileExists(name));
}


void writeFrames(string input, int count){
    std::ofstream out(input + "input.txt");
    for(int x = 1; x < count; x++){
        out << input << "outputs/output_" << x << ".jpg" << endl;
    }
    out.close(); 
}


#endif /* SEPERATOR_H */

