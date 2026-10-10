#Creates the workload for the simulators.
# What is does
# Launches 10 real processes that each burn a known amout of CPU time 
#on one core, lets the OS schedule them, and records what happened.


#Functions

import os
import time
import random
import multiprocessing
import psutil

def make_specs():
    #makes the specs for the workload
    specs = []
    rng = random.Random(42)
    for i in range(10):
        specs.append((i,rng.uniform(0.5, 5.0), 1))
    return specs

def burn(cpu_seconds):
    startTime = time.process_time()
    while cpu_seconds > (time.process_time() - startTime):
        pass

def worker(worker_id, burst):
    psutil.Process().cpu_affinity([0]) #binds the process to core 0
    startTime = time.perf_counter()
    CPUTime = time.process_time()
    #burns the CPU for burst seconds
    burn(burst)
    endTime = time.perf_counter()
    CPUEndTime = time.process_time()
    print({"WorkerID": worker_id, "PID":os.getpid(), "Burst": burst, "StartTime": startTime, "EndTime": endTime, "CPU_Used": (CPUEndTime - CPUTime)})
    
if __name__ == "__main__":
    specs = make_specs()
    workers = []
    for spec in specs:
        p = multiprocessing.Process(target=worker, args=(spec[0], spec[1]))
        p.start()
        workers.append(p)
    for p in workers:
        p.join()
        
    
    
