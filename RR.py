from collections import deque
from Process import Process
from harvest import harvest_processes
from CSVCreate import csv_creation, slices_csv

quantum = 2

def rr_schedule(processes, quantum=quantum):
    queue = deque(sorted(processes, key=lambda p: p.arrival))
    time = 0
    scheduled = []
    remaining = {p.pid: p.burst for p in processes}

    while queue:
        process = queue.popleft()
        if process.start is None:
            process.start = max(time, process.arrival)
        time = max(time, process.start)
        slice_ = min(quantum, remaining[process.pid])
        process.slices.append((time, time + slice_))
        time += slice_
        remaining[process.pid] -= slice_
        process.completion = time

        if remaining[process.pid] > 0:
            queue.append(process)
        else:
            scheduled.append(process)

    return scheduled

if __name__ == "__main__":
    procs, dropped = harvest_processes()
    scheduled = rr_schedule(procs)
    csv_creation(scheduled, "CSV_RR.csv")
    slices_csv(scheduled, "CSV_RR_Slices.csv")

    total_wait = 0
    total_turnaround = 0
    for proc in scheduled:
        print(proc)
        total_wait += proc.wait_time()
        total_turnaround += proc.turnaround_time()

    n = len(scheduled)
    print(f"Average Wait Time: {total_wait / n:.2f}")
    print(f"Average Turnaround Time: {total_turnaround / n:.2f}")