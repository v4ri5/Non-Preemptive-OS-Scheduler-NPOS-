import psutil
import time
from Process import Process


# Number of processes we want to harvest
PROCESS_LIMIT = 12


def harvest_processes():
    processes = []
    dropped_log = []

    # Time when the computer was booted
    floor = psutil.boot_time()

    # ---------------------------------------------------------
    # STEP 1:
    # Collect ALL valid processes first.
    #
    # Do NOT stop after finding 12 because we need to examine
    # every process before determining which 12 have arrival
    # times closest together.
    # ---------------------------------------------------------
    for proc in psutil.process_iter([
        'pid',
        'create_time',
        'cpu_times',
        'num_threads',
        'nice'
    ]):

        try:
            cpu_times = proc.info['cpu_times']

            # Skip process if CPU information is unavailable
            if cpu_times is None:
                continue

            pid = proc.info['pid']

            # Actual time this OS process was created
            arrival = proc.info['create_time']

            # Total CPU time used by the process
            burst = (
                cpu_times.user
                + cpu_times.system
            )

            threads = proc.info['num_threads']

            # Get priority
            priority = (
                proc.info['nice']
                if proc.info['nice'] is not None
                else 0
            )

            # Average CPU utilization since the process was created
            elapsed = time.time() - arrival
            cpu_util = (
                (burst / elapsed) * 100
                if elapsed > 0
                else 0
            )

            # -------------------------------------------------
            # Filter processes we don't want
            # -------------------------------------------------

            # Ignore processes with almost no CPU time
            if burst < 0.01:
                dropped_log.append(
                    (pid, burst, arrival)
                )
                continue

            # Ignore anything with an invalid creation time
            if arrival < floor:
                dropped_log.append(
                    (pid, burst, arrival)
                )
                continue

            # Add valid process
            processes.append(
                Process(
                    pid,
                    arrival,
                    burst,
                    threads,
                    priority,
                    cpu_util
                )
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            # Processes can disappear while we're harvesting.
            # Just skip them.
            continue

    # ---------------------------------------------------------
    # STEP 2:
    # Sort every valid process by arrival time.
    # ---------------------------------------------------------
    processes.sort(key=lambda p: p.arrival)

    # ---------------------------------------------------------
    # STEP 3:
    # Find the group of 12 consecutive processes whose
    # arrival times have the smallest overall span.
    # ---------------------------------------------------------

    if len(processes) > PROCESS_LIMIT:

        best_start = 0
        smallest_span = float("inf")

        # Slide a window of 12 processes through the sorted list
        for i in range(
            len(processes) - PROCESS_LIMIT + 1
        ):

            first_process = processes[i]

            last_process = processes[
                i + PROCESS_LIMIT - 1
            ]

            # Difference between the latest and earliest
            # arrival in this group
            span = (
                last_process.arrival
                - first_process.arrival
            )

            # If this group is closer together than the
            # previous best group, remember it
            if span < smallest_span:
                smallest_span = span
                best_start = i

        # Keep only the best group
        processes = processes[
            best_start:
            best_start + PROCESS_LIMIT
        ]

    # ---------------------------------------------------------
    # STEP 4:
    # Normalize arrival times.
    #
    # Earliest selected process becomes arrival time 0.
    # All other arrival times remain relative to it.
    # ---------------------------------------------------------

    if processes:

        earliest_arrival = processes[0].arrival

        for process in processes:
            process.arrival -= earliest_arrival

    # ---------------------------------------------------------
    # STEP 5:
    # Return selected processes and dropped processes
    # ---------------------------------------------------------

    return processes, dropped_log