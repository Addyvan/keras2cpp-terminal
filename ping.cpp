#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>

int main()
{
    const auto model = fdeep::load_model("./fdeep_ping.json");

    fdeep::tensor5 input_data(fdeep::shape5(1, 1, 1, 420, 6), 0);
    input_data.set(0, 0, 0, 0, 0, 1);
    input_data.set(0, 0, 1, 0, 0, 2);
    input_data.set(0, 0, 2, 0, 0, 3);

    for (int i = 0; i < 420; i++) {
        for (int j = 0; j < 6; j++) {
            input_data.set(0, 0, 0, i, j, 1);
        }
    }

    const auto result = model.predict(
        {input_data});
    std::cout << fdeep::show_tensor5s(result) << std::endl;

    return 0;
}