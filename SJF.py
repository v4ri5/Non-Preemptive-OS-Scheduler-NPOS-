from Process import Process 
from harvest import harvest_processes
import time

def non_preemptive_sjf(processes):
    current_time = 0
    #list of processes that have arrived
    ready_queue = []
    #keeps track of the next process in the list
    next_process = 0
    #tracks completed tasks
    completed = []


    #Sorts the processes by arrival time and burst
    processes.sort(key=lambda x: (x.arrival, x.burst))


#sort through processes in list, put them into ready queue when they arrive, execute processes based on burst one at a time
    while next_process < len(processes) or ready_queue:
        while(next_process < len(processes) and processes[next_process].arrival <= current_time):
            ready_queue.append(processes[next_process])
            next_process += 1
        
        #if nothing in ready queue, advance time
        if not ready_queue:
            current_time += 0.01
            continue

        #sort ready queue for shortes burst
        ready_queue.sort(key=lambda y: (y.burst))
        current = ready_queue.pop(0)

        #record start and finish time for jobs
        current.start = current_time
        current.completion = current_time + current.burst

        #chages state of process to terminated
        current.state = "terminated"

        #run process to completing
        current_time = current.completion

        completed.append(current)

    return completed
    

