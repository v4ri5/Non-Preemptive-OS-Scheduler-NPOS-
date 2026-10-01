from Process import Process
from harvest import harvest_processes
import csv
from SJF import non_preemptive_sjf

def csv_creation(processes, filename = "results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        #makes the header row
        writer.writerow([
            "PID", "Arrival Time", "Burst Time", "Threads", "Start Time",
            "Completion Time", "Waiting Time", "Turnaround Time",
            "Response Time", "State"
            ])
        
        #writes data for rows
        for p in processes:
            writer.writerow([
                p.pid, round(p.arrival, 2), round(p.burst, 2), p.threads,
                round(p.start, 2), round(p.completion, 2), round(p.wait_time(), 2),
                round(p.turnaround_time(), 2), round(p.response_time(), 2), p.state
            ])


processes = harvest_processes()

completed = non_preemptive_sjf(processes)

for p in completed:
    print(p)

    csv_creation(completed,"results9_10_26.csv")

#tells us total time to complete algorithm
total_time = max(p.completion for p in completed)
print(f"\nTotal scheduling time: {total_time:.2f}")