from __future__ import print_function
import sys
from subprocess import Popen, PIPE
import random

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class KerasCPPModel:
    def __init__(self, process_command="./fdeep_ping.json"):
        self.process_command = "./rl_agent_prod/keras_model " + process_command
        self._run_cpp_instance()

    def _run_cpp_instance(self):
        self.proc = Popen(self.process_command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        while True:
            line = self.proc.stderr.readline().decode("utf-8")
            if line.find("Waiting for line") != - 1:
                break
            
        eprint("model initialized to python")

    def order_predictions(self, predictions):
        sorted_preds = [i[0] for i in sorted(enumerate(predictions), key=lambda x:x[1], reverse=True)]

        return sorted_preds

    def parse_results(self, data):
        data = data.decode('utf-8')
        data = data.split("\n")[0].replace("[", "").replace("]", "").replace("output: ", "")
        predictions = [float(pred.replace(" ", "")) for pred in data.split(",")]
        ordered_predictions = self.order_predictions(predictions)
        return ordered_predictions

    def predict(self, state):
        state_string = ""
        for row in state:
            for val in row:
                state_string += str(val) + ","
        state[: -1] # remove trailing comma
        state += "\n"
        write = self.proc.stdin.write(str(state_string).encode('utf-8'))
        #self.proc.stdin.flush()
        
        #while self.proc.poll() is None:
        #    output = self.proc.stderr.readline()
        #    print("HERE  ", output)

        outs, errs = self.proc.communicate()
            

        #return self.parse_results(errs.decode('utf-8').encode('utf-8'))

    def shut_off(self):
        self.proc.stdin.write("END_GAME".encode('utf-8'))


if __name__ == "__main__":
    print("loading model")
    model = KerasCPPModel("./rl_agent_prod/fdeep_ping.json")
    print("model loaded")
    state = [[random.randint(0,3) for j in range(6)] for i in range(420)]
    print("making prediction")
    model.predict(state)
    
