import sys
from subprocess import Popen, PIPE

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_results(arr, data):
    predictions = []
    for char in data:
        if is_number(char):
            predictions.append(int(char)) 
    return predictions

def _read_output(proc):
    return_code = proc.poll()
    out, err = out_line, err_line = "",""
    while proc.poll() == None:
        out_line = proc.stdout.readline().decode('utf-8')
        if out_line[0:6] == "outline":
            data = out_line[8:]
            predictions = parse_results(data)

    print("predictions: ", predictions)


    return ( out, err )

process_command = "./main"
proc = Popen(process_command, shell=True, stdout=PIPE, stderr=sys.stderr, stdin=PIPE)

try:
    while proc.returncode == None:
        outs , errs = _read_output(proc)
except:
    print("TimeoutExpired: \n")
    outs, errs = proc.communicate()
    print("OUTS: ", outs, "ERRS: ", errs)