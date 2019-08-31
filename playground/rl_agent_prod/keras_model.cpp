#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>


int main(int argc, char** argv)
{
    const auto bit_macro = fdeep::load_model("./rl_agent_prod/bits_macro.json");
    bool game = true;
    std::string input_string;
    
    std::getline (std::cin, input_string); // get state
    float bits = std::stod(input_string.substr(0,1));
    float cores = std::stod(input_string.substr(1,1));
    std::cout << "cores: " << cores << " bits: " << bits << std::endl;

    // create state input
    int index = 0;
    fdeep::tensor5 state(fdeep::shape5(1, 1, 1, 420, 6), 0);
    for (int i = 0; i < 420; i++) {
        for (int j = 0; j < 6; j++) {
            state.set(0, 0, 0, i, j, input_string[index+2]);
            index++;
        }
    }

    // bits macro
    std::vector<int> bits_sequence;
    
    while (bits >= 1) {
        const auto result = bit_macro.predict({state});
        std::cout << fdeep::show_tensor5s(result) << std::endl;
        bits -= 1;
    }

    //std::cerr << "output: " << fdeep::show_tensor5s(result) << "\n";

    return 0;
}