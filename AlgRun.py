#Run each algorithm seperatley
from Process import Process
from harvest import harvest_processes
import csv
from SJF import non_preemptive_sjf
from RR import rr_schedule
from FCFS import fcfs_schedule
from PrioritySchedule import priority_scheduling
from CSVCreate import csv_creation, slices_csv
import time

startTime = time.perf_counter()

#harvest processes
hProcesses, dropped = harvest_processes()

#run harvested processes through SJF
completedSJF = non_preemptive_sjf(hProcesses)

csv_creation(completedSJF,"CSV_SJF.csv")

#FCFS
completedFCFS = fcfs_schedule(hProcesses)

csv_creation(completedFCFS,"CSV_FCFS.csv")

#Priority
completedPriority = priority_scheduling(hProcesses)

csv_creation(completedPriority,"CSV_Priority.csv")

#Round Robin
completedRR = rr_schedule(hProcesses)

csv_creation(completedRR,"CSV_RR.csv")
slices_csv(completedRR,"CSV_RR_Slices.csv")

endTime = time.perf_counter()

#tells us the total time this took to run
totalTime = endTime - startTime

print(f"Total time Non-Concurrent = {totalTime:.4f}")