#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>

int main()
{
  const auto model = fdeep::load_model("./fdeep_ping.json");
  vector< vector<int> > input_data(420);
  for (int i = 0; i < 420; i++) {
      input_data[i] = vector<int>(6);
      for (int j = 0; j < 6; j++) {
          input_data[i][j] = 3;
      }
  }
  fdeep::tensor5 input_tensor = fdeep::tensor5(fdeep::shape5(1,1,1,420,6), input_data);
  //const auto result = model.predict({fdeep::tensor5(fdeep::shape5(1, 1, 1, 1, 4), {1, 2, 3, 4})});
  //std::cout << fdeep::show_tensor5s(result) << std::endl;
  return 0;
}