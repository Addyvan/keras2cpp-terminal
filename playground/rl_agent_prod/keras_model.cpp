#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

int main(int argc, char** argv)
{
    //std::cout<< "You have entered " << argv[1] << std::endl ;
    const auto model = fdeep::load_model(argv[1]);

    bool game = true;
    std::string input_string;
    while (game) {
        //std::cout << "Waiting to receive state" << std::endl;
        std::cerr<< "Waiting for line" << std::endl;

        std::getline (std::cin, input_string);

        std::cout << "Received state!" << std::endl;
        if (input_string != "END_GAME") {
            float string_num = std::stod(input_string.substr(0,1));

            fdeep::tensor5 input_data(fdeep::shape5(1, 1, 1, 420, 6), 0);

            int index = 0;
            for (int i = 0; i < 420; i++) {
                for (int j = 0; j < 6; j++) {
                    input_data.set(0, 0, 0, i, j, input_string[index]);
                    index++;
                }
            }

            const auto result = model.predict({input_data});
            std::cerr << "output: " << fdeep::show_tensor5s(result) << std::endl;
            //input_string = "";
            game = false; // since we are currently YOLO just negate this logic for now
        } else {
            game = false;
        }
        
    }

    //std::cout << "Shutdown model, game ended" << std::endl;
    

    return 0;
}