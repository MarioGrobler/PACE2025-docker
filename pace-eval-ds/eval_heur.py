import subprocess
import time
import os
import signal

SOLVER_COMMAND = ["python3", "./ds_greedy.py"]     # how to invoke the solver
VERIFIER_COMMAND = ["python3", "./ds_verifier.py"] # the verifier is provided as a python3 script
INSTANCES_DIR = "./instances"                      # path to the instances
OUTPUT_DIR = "./outputs"                           # created by this script
RESULTS_FILE = "./results.csv"                     # created by this script

TIME_LIMIT = 5 * 60  # max solver time in seconds
MERCY_TIME = 25      # time between SIGTERM and SIGKILL, in seconds

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(RESULTS_FILE, "w") as result_file:
    result_file.write("instance,status,time,solution_size,error\n")

    for instance_file in sorted(os.listdir(INSTANCES_DIR)):
        instance_path = os.path.join(INSTANCES_DIR, instance_file)
        output_path = os.path.join(OUTPUT_DIR, f"{instance_file}.sol")

        try:
            start = time.time()
            proc = subprocess.Popen(
                ["taskset", "-c", "0"] + SOLVER_COMMAND + [instance_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = proc.communicate(timeout=TIME_LIMIT)
                end = time.time()
                runtime = end - start
            except subprocess.TimeoutExpired:
                proc.send_signal(signal.SIGTERM)
                try:
                    stdout, stderr = proc.communicate(timeout=MERCY_TIME)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    stdout, stderr = proc.communicate()
                result_file.write(f"{instance_file},TIMEOUT,,,\n")
                continue

            if proc.returncode != 0:
                result_file.write(f"{instance_file},RUNTIME_ERROR,,,{stderr.strip()}\n")
                continue
            
            with open(output_path, "w") as out_file:
                out_file.write(stdout)

            verifier = subprocess.run(
                VERIFIER_COMMAND + [instance_path, output_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if verifier.returncode == 0:
                sol_size = int(verifier.stdout.strip())
                result_file.write(f"{instance_file},OK,{runtime:.2f},{sol_size},\n")
            elif verifier.returncode == -1:
                # verifier reports error
                result_file.write(f"{instance_file},INVALID_SOLUTION,{runtime:.2f},,VerifierError: {verifier.stderr.strip()}\n")
            else:
                # something went totally wrong
                result_file.write(f"{instance_file},VERIFIER_ERROR,{runtime:.2f},,ReturnCode: {verifier.returncode}, {verifier.stderr.strip()}\n")

        except Exception as e:
            result_file.write(f"{instance_file},EXCEPTION,,,{str(e)}\n")

print("End")