#! /usr/bin/python

import csv
import os
import re
import subprocess
import sys

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def get_num_after(text, substr):
    """searches text for substr, and returns the first number that follows"""
    regex = r'\d+\.?\d*'
    for line in text.splitlines():
        if substr in line:
            line = line[line.find(substr):] # everything after substr
            all_matches = re.findall(regex, line)
            return float(all_matches[0])
    return float(-1)

GPU_KERNEL_KEY = "gpu_kernel"
CPU_KERNEL_KEY = "cpu_kernel"
TOTAL_PROXIES_KEY = "total_prox"
H2D_KEY = "h2d"
D2H_KEY = "d2h"

base_terms = {
    "init"       : "Initialization",
    "alloc"      : "Allocation",
    GPU_KERNEL_KEY : "Kernel",
    "dealloc"    : "Dealloc"
}

custom_type_terms = {
    "CUDA-D" : {
        H2D_KEY : "Copy To",
        D2H_KEY : "Copy Back"
    }
}

custom_exe_terms = {
    "cedd" : {
        GPU_KERNEL_KEY    : "GPU Proxy: Kernel",
        CPU_KERNEL_KEY    : "CPU Proxy: Kernel",
        TOTAL_PROXIES_KEY : "Total Proxies"
    },
    "cedt" : {
        GPU_KERNEL_KEY : "GPU Proxy: Kernel",
        CPU_KERNEL_KEY : "CPU Proxy: Kernel",
        TOTAL_PROXIES_KEY : "Total Proxies"
    }
}

def get_row(num, text, header, search_terms):
    row_out = [num]
    for k in header[1:]: # skip "row"
        search_term = search_terms[k]
        row_out = row_out + [get_num_after(text, search_term)]
    return row_out

if len(sys.argv) < 2:
    print "Expected an argument"
    sys.exit(-1)



BENCH_PATH = sys.argv[1]
TYPE = os.path.split(BENCH_PATH)[0]
EXE = os.path.split(BENCH_PATH)[1]
EXE = EXE.lower()


print BENCH_PATH, "->", EXE
print "TYPE:", TYPE
print "EXE:", EXE

os.environ["CHAI_CUDA_LIB"] = "/usr/local/cuda/lib64"
os.environ["CHAI_CUDA_INC"] = "/usr/local/cuda/include"

with open(EXE+".csv", 'w') as csvfile:

    # Start with base terms
    search_terms = base_terms

    # Add or override any base on the benchmark type
    if TYPE in custom_type_terms:
        custom_terms = custom_type_terms[TYPE]
        for k in custom_terms:
            search_terms[k] = custom_terms[k]

    # Add or override any terms based on the benchmark
    if EXE in custom_exe_terms:
        custom_terms = custom_exe_terms[EXE]
        for k in custom_terms:
            search_terms[k] = custom_terms[k]


    print search_terms

    header = ["run"] + [k for k in search_terms]
    print header

    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)

    with cd(BENCH_PATH):
        rel_exe = os.path.join("./", EXE)

        if not os.path.isfile(rel_exe):
            print "couldn't find", rel_exe
            subprocess.call("make")

        for i in range(10):
            process = subprocess.Popen([rel_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print out
            row = get_row(i, out, header, search_terms)
            print row
            writer.writerow(row)
    csvfile.close()

