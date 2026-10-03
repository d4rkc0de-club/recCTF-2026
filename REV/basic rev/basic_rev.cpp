#include <iostream>
#include <string>

int main(int argc, char *argv[]) {
    if (argc != 2){
        std::cout << "Pass the flag as an cmd line argument." << "\n";
        return 1;
    }
    std::string f = argv[1];

    if (f.length() != 29)
        return 1;

    if (f[0] != 'd') return 1;
    if (f[1] != '4') return 1;
    if (f[2] != 'r') return 1;
    if (f[3] != 'k') return 1;
    if (f[4] != '{') return 1;
    if (f[5] != 's') return 1;
    if (f[6] != 't') return 1;
    if (f[7] != 'e') return 1;
    if (f[8] != '4') return 1;
    if (f[9] != 'd') return 1;
    if (f[10] != 'y') return 1;
    if (f[11] != '_') return 1;
    if (f[12] != 'b') return 1;
    if (f[13] != '3') return 1;
    if (f[14] != 'g') return 1;
    if (f[15] != '1') return 1;
    if (f[16] != 'n') return 1;
    if (f[17] != 'n') return 1;
    if (f[18] != '1') return 1;
    if (f[19] != 'n') return 1;
    if (f[20] != 'g') return 1;
    if (f[21] != 's') return 1;
    if (f[22] != '_') return 1;
    if (f[23] != '2') return 1;
    if (f[24] != '5') return 1;
    if (f[25] != '2') return 1;
    if (f[26] != '2') return 1;
    if (f[27] != 'a') return 1;
    if (f[28] != 'd') return 1;
    if (f[29] != '}') return 1;

    std::cout << "Correct!\n";
}