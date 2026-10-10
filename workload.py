#Creates the workload for the simulators.
# What is does
# Launches 10 real processes that each burn a known amout of CPU time 
#on one core, lets the OS schedule them, and records what happened.


#Functions

import time


def burn(cpu_seconds):
    startTime = time.process_time()
    while cpu_seconds > (time.process_time() - startTime):
        
        pass

if __name__ == "__main__":
    performance = time.perf_counter()
    burn(2)
    print("Time taken to burn 2 seconds of CPU time: ", time.perf_counter() - performance)