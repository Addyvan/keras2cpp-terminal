import sys
from subprocess import Popen, PIPE,TimeoutExpired

def _read_output(proc):
    return_code = proc.poll()
    out, err = out_line, err_line = "",""
    while proc.poll() == None:
        out_line = proc.stdout.readline().decode('utf-8')
        print(out_line)

    return ( out, err )

process_command = "./main"
proc = Popen(process_command, shell=True, stdout=PIPE, stderr=sys.stderr, stdin=PIPE)

try:
    while proc.returncode == None:
        outs , errs = _read_output(proc)
except TimeoutExpired:
    print("TimeoutExpired: \n")
    outs, errs = proc.communicate()
    print("OUTS: ", outs, "ERRS: ", errs)