from Process import Process
from harvest import harvest_processes
import csv
from SJF import non_preemptive_sjf
from CSVCreate import csv_creation
processes, dropped = harvest_processes()

completed = non_preemptive_sjf(processes)

for p in completed:
    print(p)

csv_creation(completed,"CSV_SJF.csv")

#tells us total time to complete algorithm
total_time = max(p.completion for p in completed)
print(f"\nTotal scheduling time: {total_time:.2f}")