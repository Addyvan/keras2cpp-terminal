#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>

int main()
{
  std::cout << "output: [1,2,3,4,5,6,7,8,9,10]" << std::endl;
  //const auto model = fdeep::load_model("./output/fdeep_model.json");
  //const auto result = model.predict({fdeep::tensor5(fdeep::shape5(1, 1, 1, 1, 4), {1, 2, 3, 4})});
  //std::cout << fdeep::show_tensor5s(result) << std::endl;
  return 0;
}