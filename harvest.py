import psutil
from Process import Process

##Collects the processes to be scheduled and their attributes from the system using the psutil library.

floor = psutil.boot_time()

def harvest_processes():
    processes = []                  #List of processes to be scheduled
    
    floor = psutil.boot_time()
    DroppedLog = []
    
    for proc in psutil.process_iter(['pid','create_time','cpu_times', 'num_threads', 'nice']): # Get process information
        try:
            cpu_times = proc.info['cpu_times']
            if cpu_times is None:
                continue

            pid = proc.info['pid']
            #removes window processes that mess up math
            arrival = proc.info['create_time']
            burst = proc.info['cpu_times'].user + proc.info['cpu_times'].system
            threads = proc.info['num_threads']
            priority = proc.info['nice'] if proc.info['nice'] is not None else 0  # Default priority to 0 if not available
            #Excludes things that dont take any cpu time and things that happen before the boot time 
            if burst < 0.01 or arrival < floor:
                DroppedLog.append((pid, burst, arrival))
                continue
            processes.append(Process(pid, arrival, burst, threads, priority))
            if len(processes) >= 10:  # Limit to 10 processes
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): ## Handles exceptions from process extra process information that we cant use 
            pass
    return processes, DroppedLog

        