FROM ubuntu:22.04

# Basic Setup
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    time \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

# working directory
WORKDIR /app
COPY . /app

# OPTIONAL: you can directly build zour solver here, eg as in the following line
# RUN g++ -O2 -std=c++17 solver.cpp -o solver

# invoke the evaluation process (choose exact or heuristic)
# CMD ["python3", "eval_exact.py"]
CMD ["python3", "eval_heur.py"] 
