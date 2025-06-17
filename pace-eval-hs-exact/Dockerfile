FROM ubuntu:22.04

# Basic Setup
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    time \
    cmake \
    git \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install openjdk-21-jdk -y

# INSTALL YOUR SOLVER AND DEPENDENCIES HERE
COPY pace-eval-hs-exact/solver/hs_greedy.py /solver/hs_greedy.py
# END OF YOUR CODE HERE.

# working directory
WORKDIR /pace
COPY ../src/eval.py eval.py
COPY ../src/hs_verifier.py verifier.py

RUN mkdir -p /output && chmod 777 /output
CMD ["python3", "eval.py"]
