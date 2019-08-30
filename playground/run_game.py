import os
import subprocess
import sys

def run_game():
    print("Running game")
    # This is only for windows
    if "run.ps1" not in algo1:
        trailing_char = "" if algo1.endswith("\\") else "\\"
        algo1 = algo1 + trailing_char + "run.ps1"
    if "run.ps1" not in algo2:
        trailing_char = "" if algo2.endswith("\\") else "\\"
        algo2 = algo2 + trailing_char + "run.ps1"

    algo1_path = os.path.abspath("./rl_agent_prod/run.sh")
    algo2_path = os.path.abspath("./rl_agent_prod/run.sh")

    process_command = "java -jar engine.jar work {} {}".format(algo1_path, algo2_path)

    p = subprocess.Popen(
        process_command,
        shell=True,
        stdout=sys.stdout,
        stderr=sys.stderr
        )
    p.daemon = 1
    p.wait()
    #listen_to_game(proc)