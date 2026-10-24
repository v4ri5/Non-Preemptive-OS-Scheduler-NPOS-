#Utilities
import Process
from workload import make_specs
import CSVCreate
from CSVCreate import csv_creation, slices_csv


#Schedulers
import FCFS
import SJF
import PrioritySchedule
import RR


def make_processes(specs):
    processes = []
    for spec in specs:
        processes.append(Process.Process(spec[0], 0, spec[1], spec[2], spec[3]))
       
    return processes

if __name__ == "__main__": 
    specs = make_specs()
    fcfs_processes = make_processes(specs)
    sjf_processes = make_processes(specs)
    priority_processes = make_processes(specs)
    RR_processes = make_processes(specs)
    
    FCFS.fcfs_schedule(fcfs_processes)
    SJF.non_preemptive_sjf(sjf_processes)
    PrioritySchedule.priority_scheduling(priority_processes)
    RR.rr_schedule(RR_processes, quantum=1)
    
    csv_creation(fcfs_processes, "CSV_Predict_FCFS.csv")
    csv_creation(sjf_processes, "CSV_Predict_SJF.csv")
    csv_creation(priority_processes, "CSV_Predict_Priority.csv")
    csv_creation(RR_processes, "CSV_Predict_RR.csv")
    slices_csv(RR_processes, "CSV_Predict_RR_Slices.csv")



