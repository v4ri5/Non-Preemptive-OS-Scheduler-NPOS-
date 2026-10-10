from collections import deque
from Process import Process
from harvest import harvest_processes
from CSVCreate import csv_creation

quantum = 2

def rr_schedule(processes, quantum=quantum):
    queue = deque(sorted(processes, key=lambda p: p.arrival))
    time = 0
    scheduled = []

    while queue:
        process = queue.popleft()
        if process.start is None:
            process.start = max(time, process.arrival)
        time = max(time, process.start)
        slice_ = min(quantum, process.burst)
        time += slice_
        process.burst -= slice_
        process.completion = time

        if process.burst > 0:
            queue.append(process)
        else:
            scheduled.append(process)

    return scheduled

if __name__ == "__main__":
    procs, dropped = harvest_processes()
    scheduled = rr_schedule(procs)
    csv_creation(scheduled, "CSV_RR.csv")

    total_wait = 0
    total_turnaround = 0
    for proc in scheduled:
        print(proc)
        total_wait += proc.wait_time()
        total_turnaround += proc.turnaround_time()

    n = len(scheduled)
    print(f"Average Wait Time: {total_wait / n:.2f}")
    print(f"Average Turnaround Time: {total_turnaround / n:.2f}")