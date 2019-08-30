#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

int main(int argc, char** argv)
{
    //std::cout<< "You have entered " << argv[1] << " for all values" << std::endl ;
    const auto model = fdeep::load_model(argv[1]);

    bool gameDone = false;
    std::string input_string;
    while (!gameDone) {
        
        std::getline (std::cin, input_string);

        //std::cout<< "HERE: " << input_string << std::endl;
        float string_num = std::stod(input_string.substr(0,1));

        fdeep::tensor5 input_data(fdeep::shape5(1, 1, 1, 420, 6), 0);

        for (int i = 0; i < 420; i++) {
            for (int j = 0; j < 6; j++) {
                input_data.set(0, 0, 0, i, j, string_num);
            }
        }

        const auto result = model.predict({input_data});
        std::cerr << "output: " << fdeep::show_tensor5s(result) << std::endl;
        input_string = "";
    }
    

    return 0;
}