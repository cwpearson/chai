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

default_search_terms = {
    "init"       : "Initialization",
    "alloc"      : "Allocation",
    "h2d"        : "Copy To",
    GPU_KERNEL_KEY : "Kernel",
    "d2h"        : "Copy Back",
    "dealloc"    : "Dealloc"
}

custom_search_terms = {
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

def get_row(exe, text, header, search_terms):
    row_out = []
    for k in header:
        search_term = search_terms[k]
        row_out = row_out + [get_num_after(text, search_term)]
    return row_out

if len(sys.argv) < 2:
    print "Expected an argument"
    sys.exit(-1)



BENCH_DIR = sys.argv[1]
EXE = os.path.split(BENCH_DIR)[-1]
EXE = EXE.lower()

print BENCH_DIR, "->", EXE

os.environ["CHAI_CUDA_LIB"] = "/usr/local/cuda/lib64"
os.environ["CHAI_CUDA_INC"] = "/usr/local/cuda/include"

with open(EXE+".csv", 'w') as csvfile:

    search_terms = {}

    # Add default search terms
    for k in default_search_terms:
        search_terms[k] = default_search_terms[k]

    # Override any default terms
    if EXE in custom_search_terms:
        for k in search_terms:
            if k in custom_search_terms[EXE]:
                search_terms[k] = custom_search_terms[EXE][k]

    # Add any custom search terms
    if EXE in custom_search_terms:
        for k in custom_search_terms[EXE]:
            if k not in default_search_terms:
                search_terms[k] = custom_search_terms[EXE][k]


    print search_terms

    header = [k for k in search_terms]

    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)

    with cd(BENCH_DIR):
        rel_exe = os.path.join("./", EXE)

        if not os.path.isfile(rel_exe):
            print "couldn't find", rel_exe
            subprocess.call("make")

        for i in range(1):
            process = subprocess.Popen([rel_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print out
            row = get_row(rel_exe, out, header, search_terms)
            print row
            writer.writerow(row)
    csvfile.close()

