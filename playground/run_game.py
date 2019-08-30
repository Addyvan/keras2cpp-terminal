import os
import subprocess
import sys

def run_game():
    print("Running game")
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
    
if __name__ == "__main__":
    run_game()