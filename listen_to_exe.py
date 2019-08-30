from __future__ import print_function
import sys
from subprocess import Popen, PIPE
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
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_results(data):
    print("parsing predictions   --- ", data)
    predictions = []
    for char in data:
        if is_number(char):
            predictions.append(int(char))
    print(predictions)
    return predictions

process_command = "./ping"
proc = Popen(process_command, shell=True, stdout=sys.stdout, stderr=PIPE, stdin=PIPE)

for i in range(5):
    outs, errs = proc.communicate(input=str(i))
    print("python outs: ", outs)
    parse_results(errs)
    time.sleep(2)


#print("python: ",  errs.decode())