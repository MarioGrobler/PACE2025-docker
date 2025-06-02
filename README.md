# Docker Environment for the PACE Challenge 2025

This repository contains two docker environments, one for the dominating set tracks and one for the hitting set tracks of the PACE Challenge 2025.
The evaluation of all solvers will take place within this environment to ensure fairness. To be precise, we provide one core and 16 GB of RAM for all solvers.

This repository contains a small demo solver and a small set of test instances for both problems.

## Getting started

First of all, install docker on your machine if not already present. Then, depending on whether you want to evaluate a dominating set solver or heuristic solver, navigate to `pace-eval-ds` or `pace-eval-hs` respectively. Then run

```bash
docker build -t pace-eval .
```

This will set up the environment. Afterwards, you can evaluate the provided demo solver by invoking

```bash
docker run --cpus="1" --memory="16g" --rm -v "$PWD":/app pace-eval
```

The provided restrictions are exactly those we will use to evaluate the solvers, in particularly only one core and 16 GB of RAM.

## How to replace the demo solver
If you would like to replace the demo solver, you need to modify some things. This depends on whether you want to run an exact solver or a heuristic solver.

### The Dockerfile
The Dockerfile runs the evaluation process for heuristic solvers per default, as specified in line 21:
```docker
CMD ["python3", "eval_heur.py"] 
```
If you want to invoke the evaluation process for exact solvers, replace the line by
```docker
CMD ["python3", "eval_exact.py"] 
```
You can also comment out this line if you don't want to invoke the evaluation process as soon as you run docker.

By the way, you can directly install your solver in the docker file, eg by running `g++` or `make`, depending on your solver (see eg the uncommented line 17). Alternatively, you can install your solver as usual.

### The evaluation scripts
This repository contains two evaluation scripts, one for exact solvers and one for heuristiv solvers. However, up to time limits they are identical. We will briefly guide you through the important parts.

Lines 6 to 10 specify the working directories and solvers
 - `SOLVER_COMMAND` is a list specifying the solver location and how to execute them. In our case it is `["python3", "./ds_greedy.py"]`, where `./ds_greedy.py` is the location of the solver while the `python3` is the executable needed to run the solver. If your solver is a single executable the list is also a singleton.
 - `VERIFIER_COMMAND` is similar to `SOLVER_COMMAND`, just for the verifier. You can leave this line untouched if you want to use the default verifier (which we will also use). Note that the default verifier does not check for optimality.
 - `INSTANCES_DIR` is the directory containing the instances the solver will be evaluated on. Note that this repository only contains three test instances. To find the public instances for PACE 2025, we refer to the [instance repository](https://github.com/MarioGrobler/PACE2025-instances).
 - `OUTPUT_DIR` is a directory that will be created to save the output of your solver.
 - `RESULTS_FILE` is the name of a CSV-file containing the result of the evaluation process (solution ok, timeout, runtime error).

The next two lines contain the time limits.
 - `TIME_LIMIT` contains the time limit per run in seconds. Default is 30min for exact solvers and 5min for heuristic solvers.
 - `MERCY_TIME` contains the mercy time in seconds, that is, the time period between sending `SIGTERM` and `SIGKILL`. Default is 25 seconds for both, the exact and heuristic track.

## Saving and loading docker containers
Once everything is set up, you can save the whole environment as an follows.

```bash
docker save pace-eval > pace-eval.tar
```

Similarly, you can load an image as follows.
```bash
docker load < pace-eval.tar
```

Afterwards, you can run it as usual (see above).