#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>

int main()
{
  const auto model = fdeep::load_model("./output/fdeep_model.json");
  std::cout<< model.get_input_shapes() <<std::endl;
  //const auto result = model.predict({fdeep::tensor5(fdeep::shape5(1, 1, 1, 1, 4), {1, 2, 3, 4})});
  //std::cout << fdeep::show_tensor5s(result) << std::endl;
  return 0;
}