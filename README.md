# Chai

## Overview

Chai is a benchmark suite of Collaborative Heterogeneous Applications for Integrated-architectures. The Chai benchmarks are designed to use the latest features of heterogeneous architectures such as shared virtual memory and system-wide atomics to achieve efficient simultaneous collaboration between host and accelerator devices.

Each benchmark has multiple implementations. This release includes the OpenCL 2.0 and OpenCL 1.2 implementations. The CUDA, CUDA-Sim, and C++AMP implementations are underway. If you would like early access to premature versions, please contact us.

## Instructions

Clone the repository:

  ```
  git clone https://github.com/chai-benchmarks/chai.git
  cd chai
  ```

Export environment variables:

  ```
  export CHAI_OCL_LIB=<path/to/OpenCL/lib>
  export CHAI_OCL_INC=<path/to/OpenCL/include>
  ```

Select desired implementation:

  ```
  cd OpenCL2.0
  ```

Select desired benchmark:

  ```
  cd BFS
  ```

Compile:

  ```
  make
  ```

Execute:

  ```
  ./bfs
  ```

For help instructions:

  ```
  ./bfs -h
  ```

## Citation

If you think this work is useful, please cite us at https://chai-benchmarks.github.io for now, until we provide another reference.

## Running OpenCL 1.2 benchmarks on NVIDIA with Docker

Install `docker` for your system.

Install `nvidia-docker`.

To build the docker image, use

    nvidia-docker build . -t chai

To run a benchmark (for example, BS), do

    nvidia-docker run -it chai bash -c "cd chai/OpenCL1.2/BS/ && ./bs"

## Docker: Running OpenCL 1.2 and 2.0 Benchmarks with the Intel OpenCL CPU Stacks
[![Build Status](https://travis-ci.org/cwpearson/chai.svg?branch=master)](https://travis-ci.org/cwpearson/chai)

Install `docker` for your system.

To build the docker image for OpenCL 1.2 and 2.0 respectively, use

    docker build . -f Dockerfile.intel_ocl1.2_cpu -t chai-intel-1.2
    docker build . -f Dockerfile.intel_ocl2.0_cpu -t chai-intel-2.0

To run a benchmark (for example, BS) from the two images, use

    docker run -it chai-intel-1.2 bash -c "cd BS/ && ./bs"
    docker run -it chai-intel-2.0 bash -c "cd BS/ && ./bs"

To run all the benchmarks, try

    docker run -it chai-intel-1.2 bash -c "test.sh"

