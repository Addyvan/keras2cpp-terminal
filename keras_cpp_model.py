from __future__ import print_function
import sys
from subprocess import Popen, PIPE


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class KerasCPPModel:
    def __init__(self, process_command="./ping"):
        self.process_command = process_command
        self._run_cpp_instance()

    def _run_cpp_instance(self):
        self.proc = Popen(self.process_command, shell=True, stdout=sys.stdout, stderr=PIPE, stdin=PIPE)
        self.proc.wait()

    def order_predictions(self, predictions):
        sorted_preds = [i[0] for i in sorted(enumerate(predictions), key=lambda x:x[1], reverse=True)]

        return sorted_preds

    def parse_results(self, data):
        data = data.decode('utf-8')
        data = data.split("\n")[0].replace("[", "").replace("]", "").replace("output: ", "")
        predictions = [float(pred.replace(" ", "")) for pred in data.split(",")]
        ordered_predictions = self.order_predictions(predictions)
        return ordered_predictions

    def predict(self, i):
        try:
            self.proc.stdin.write(str(i).encode('utf-8'))
            outs, errs = self.proc.communicate()
        except:
            print("TIMEOUT")
            outs, errs = proc.communicate()
        return parse_results(errs)


if __name__ == "__main__":
    model = KerasCPPModel()
    print("model loaded")
    predictions = model.predict(1)
    print("predictions: ", predictions)