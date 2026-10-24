# The processes to be scheduled is defined in this file. 
# The Process class represents a process with its attributes 
# and methods to calculate turnaround time, wait time, and response time.
import psutil
class Process:
    def __init__(self, pid, arrival, burst, threads, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.threads = threads
        self.priority = priority
        self.start = None
        self.completion = None
        self.state = "new"
        self.slices = [] 


    def turnaround_time(self):
        return self.completion - self.arrival

    def wait_time(self):
        return self.turnaround_time() - self.burst

    def response_time(self):
        return self.start - self.arrival

    def __repr__(self):
        return (f"Process {self.pid}: "
               f"Arrival={self.arrival:.2f}, "
               f"Burst={self.burst:.2f}, "
               f"Start={self.start:.2f}, "
               f"Completion={self.completion:.2f}, "
               f"Waiting Time: {self.wait_time():.2f}, "
               f"Turnaround Time: {self.turnaround_time():.2f}, "
               f"Response Time: {self.response_time():.2f}, "
               f"State={self.state}")
