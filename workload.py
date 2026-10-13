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
import csv
import platform

def write_csv(results, release_time, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=['PID', 'Start Time', 'Completion Time', 'OS PID','Burst Time','Response Time','Turnaround Time', 'CPU Used', 'OS'])
        writer.writeheader()
        for r in results:
            row = {
                "OS PID": r["OS PID"],
                "Start Time": r["StartTime"] - release_time,
                "Completion Time": r["EndTime"] - release_time,
                "PID": r["PID"],
                "Burst Time": r["Burst"],
                "Response Time": r["StartTime"] - release_time,
                "Turnaround Time": r["EndTime"] - release_time,
                "CPU Used": r["CPU_Used"],
                "OS": platform.system()
            }
            writer.writerow(row)

        
def make_specs():
    #makes the specs for the workload
    specs = []
    rng = random.Random(42)
    for i in range(12): # Creates 12 processes with random burst times between 0.5 and 5 seconds
        specs.append((i,rng.uniform(1, 10), 1, rng.randint(1,5))) # (PID, Burst Time, Threads, Priority)
    return specs

def burn(cpu_seconds):
    startTime = time.process_time()
    while cpu_seconds > (time.process_time() - startTime):
        pass

def worker(start_event, worker_id, burst, results):
    psutil.Process().cpu_affinity([0]) #binds the process to core 0
    start_event.wait()  # Wait for the start event
    startTime = time.perf_counter()
    CPUTime = time.process_time()
    #burns the CPU for burst seconds
    burn(burst)
    endTime = time.perf_counter()
    CPUEndTime = time.process_time()
    results.put({"OS PID": os.getpid(), "PID":worker_id, "Burst": burst, "StartTime": startTime, "EndTime": endTime, "CPU_Used": (CPUEndTime - CPUTime)})

def run_workload(specs):
    workers = []
    start_event = multiprocessing.Event()
    results = multiprocessing.Queue()
    for spec in specs:
        p = multiprocessing.Process(target=worker, args=(start_event, spec[0], spec[1], results))
        p.start()
        workers.append(p)
    time.sleep(2)
    release_time = time.perf_counter()
    start_event.set()  # Signal all workers to start
    collected = []
    for spec in specs:
        collected.append(results.get())  # Wait for all workers to finish
    for p in workers:
        p.join()
    return collected, release_time


if __name__ == "__main__":
    specs = make_specs()
    collected, release_time = run_workload(specs)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "CSV_Workload.csv")
    write_csv(collected, release_time, csv_path)
    
    print(f"Workload completed. Results written to {csv_path}")
    
        
    
    
