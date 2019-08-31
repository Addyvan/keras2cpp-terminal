from __future__ import print_function
import sys
from subprocess import TimeoutExpired, Popen, PIPE
import time
"""
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _read_output(proc):
    return_code = proc.poll()
    out, err = out_line, err_line = "",""
    while proc.poll() == None:
        out_line = proc.stderr.readline().decode('utf-8').encode('utf-8')
        print("SUH -- ", out_line)
        
        if len(out_line) >= 0:
            if out_line.find("output") != - 1:
                data = out_line[8:]
                predictions = parse_results(data)
                print("predictions: ", predictions)
            else:
                print("NOPE: ", out_line)
            out.append(out_line)
        
    return ( out, err )

process_command = "./ping 1"
proc = Popen(process_command, shell=True, stdout=sys.stdout, stderr=sys.stderr, stdin=PIPE)

try:
    while proc.returncode == None:
        outs , errs = _read_output(proc)
except:
    outs, errs = proc.communicate()
"""


def order_predictions(predictions):
    sorted_preds = [i[0] for i in sorted(enumerate(predictions), key=lambda x:x[1], reverse=True)]

    return sorted_preds

def parse_results(data):
    data = data.decode('utf-8')
    data = data.split("\n")[0].replace("[", "").replace("]", "").replace("output: ", "")
    predictions = [pred.replace(" ", "") for pred in data.split(",")]
    print(predictions)
    #ordered_predictions = self.order_predictions(predictions)
    #return ordered_predictions

process_command = "./keras_model ./fdeep_ping.json"
proc = Popen(process_command, shell=True, stdout=sys.stdout, stderr=PIPE, stdin=PIPE)
for i in range(5):
    try:
        proc.stdin.write(str(i).encode('utf-8'))
        #outs, errs = proc.communicate()
        errs = proc.stderr.readlines(2)
    except TimeoutExpired:
        #proc.kill()
        outs, errs = proc.communicate()


    parse_results(errs)
    time.sleep(2)


#print("python: ",  errs.decode())