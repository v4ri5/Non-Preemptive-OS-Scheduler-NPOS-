from Process import Process
from harvest import harvest_processes
import csv
import os
from SJF import non_preemptive_sjf

# folder this file lives in, so CSVs always land in the project folder
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def project_path(filename):
    return os.path.join(PROJECT_DIR, filename)

def csv_creation(processes, filename = "resultsSJF.csv"):
    with open(project_path(filename), mode="w", newline="") as file:
        writer = csv.writer(file)

        #makes the header row
        writer.writerow([
            "PID", "Arrival Time", "Burst Time", "Threads", "Start Time",
            "Completion Time", "Waiting Time", "Turnaround Time",
            "Response Time", "CPU Utilization"
            ])
        
        #writes data for rows
        for p in processes:
            writer.writerow([
                p.pid, round(p.arrival, 2), round(p.burst, 2), p.threads,
                round(p.start, 2), round(p.completion, 2), round(p.wait_time(), 2),
                round(p.turnaround_time(), 2), round(p.response_time(), 2), f"{p.cpu_percent:.8f}"
            ])


def custom_csv_creation(processes, filename = "resultsSJF.csv"):
    with open(project_path(filename), mode="w", newline="") as file:
        writer = csv.writer(file)

        #makes the header row
        writer.writerow([
            "PID", "Arrival Time", "Burst Time", "Threads", "Start Time",
            "Completion Time", "Waiting Time", "Turnaround Time",
            "Response Time"
            ])
        
        #writes data for rows
        for p in processes:
            writer.writerow([
                p.pid, round(p.worker_arrival, 2), round(p.worker_burst, 2), p.worker_threads,
                round(p.worker_start, 2), round(p.worker_completion, 2), round(p.wait_time(), 2),
                round(p.turnaround_time(), 2), round(p.response_time(), 2)
            ])


def slices_csv(processes, filename = "CSV_RR_Slices.csv"):
    with open(project_path(filename), mode="w", newline="") as file:
        writer = csv.writer(file)

        #makes the header row
        writer.writerow(["PID", "Start", "End"])

        #writes one row per time slice
        for p in processes:
            for start, end in p.slices:
                writer.writerow([p.pid, round(start, 2), round(end, 2)])