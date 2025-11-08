#Leysha Antenor - ChatGPT project

#!/usr/bin/env python3
import sys
from collections import deque

class Process:
    def __init__(self, name, arrival, burst):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start_time = None
        self.completion_time = None

def read_input(filename):
    params = {}
    processes = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if parts[0] == "processcount":
                    params['processcount'] = int(parts[1])
                elif parts[0] == "runfor":
                    params['runfor'] = int(parts[1])
                elif parts[0] == "use":
                    params['use'] = parts[1]
                elif parts[0] == "quantum":
                    params['quantum'] = int(parts[1])
                elif parts[0] == "process":
                    # expected format: process name X arrival Y burst Z
                    kwargs = {}
                    i = 1
                    while i < len(parts):
                        key = parts[i]
                        val = parts[i+1]
                        kwargs[key] = val
                        i += 2
                    if 'name' not in kwargs:
                        print("Error: Missing parameter name.")
                        sys.exit(1)
                    if 'arrival' not in kwargs:
                        print("Error: Missing parameter arrival.")
                        sys.exit(1)
                    if 'burst' not in kwargs:
                        print("Error: Missing parameter burst.")
                        sys.exit(1)
                    processes.append(Process(kwargs['name'], int(kwargs['arrival']), int(kwargs['burst'])))
                elif parts[0] == "end":
                    break
    except FileNotFoundError:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)

    # Validation
    if 'use' not in params:
        print("Error: Missing parameter use.")
        sys.exit(1)
    if params['use'] == "rr" and 'quantum' not in params:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    return params, processes

def print_header(processes, algo, quantum=None):
    if algo == "fcfs":
        algo_name = "First Come First Served"
    elif algo == "sjf":
        algo_name = "preemptive Shortest Job First"
    elif algo == "rr":
        algo_name = "Round-Robin"
    else:
        algo_name = algo
    print(f"{len(processes)} processes")
    print(f"Using {algo_name}")
    if algo == "rr":
        print(f"Quantum {quantum}")
    print()  # blank line before timeline

def print_summary(processes, runfor):
    print(f"Finished at time {runfor}\n")
    for p in sorted(processes, key=lambda x: x.name):
        turnaround = p.completion_time - p.arrival
        wait = turnaround - p.burst
        response = p.start_time - p.arrival
        print(f"{p.name} wait {wait:3} turnaround {turnaround:3} response {response}")

def fcfs(processes, runfor):
    time = 0
    ready = []
    processes_left = processes[:]
    processes_left.sort(key=lambda p: p.arrival)
    current = None

    while time < runfor:
        # Check arrivals at this time
        for p in processes_left[:]:
            if p.arrival == time:
                print(f"Time {time:3} : {p.name} arrived")
                ready.append(p)
                processes_left.remove(p)

        if current is None and ready:
            current = ready.pop(0)
            if current.start_time is None:
                current.start_time = time
            print(f"Time {time:3} : {current.name} selected (burst {current.remaining:3})")

        if current:
            current.remaining -= 1
            if current.remaining == 0:
                current.completion_time = time + 1
                print(f"Time {time+1:3} : {current.name} finished")
                current = None
        else:
            print(f"Time {time:3} : Idle")

        time += 1

    return processes


def sjf_preemptive(processes, runfor):
    time = 0
    ready = []
    processes_left = processes[:]
    last_running = None

    while time < runfor:
        # arrivals at current time
        for p in processes_left[:]:
            if p.arrival == time:
                print(f"Time {time:3} : {p.name} arrived")
                ready.append(p)
                processes_left.remove(p)

        if ready:
            ready.sort(key=lambda x: x.remaining)
            current = ready[0]
            # print selection only when dispatch changes (keep as preemptive SJF behavior)
            if current != last_running:
                print(f"Time {time:3} : {current.name} selected (burst {current.remaining:3})")
                if current.start_time is None:
                    current.start_time = time
            current.remaining -= 1
            if current.remaining == 0:
                current.completion_time = time + 1
                print(f"Time {time+1:3} : {current.name} finished")
                ready.remove(current)
                last_running = None
            else:
                last_running = current
        else:
            print(f"Time {time:3} : Idle")
            last_running = None
        time += 1

    return processes

def round_robin(processes, runfor, quantum):
    time = 0
    queue = deque()
    processes_left = processes[:]

    while time < runfor:
        # arrivals at current time
        for p in processes_left[:]:
            if p.arrival == time:
                print(f"Time {time:3} : {p.name} arrived")
                queue.append(p)
                processes_left.remove(p)

        if queue:
            current = queue.popleft()
            # print a selection on every dispatch (even if same process as last quantum)
            print(f"Time {time:3} : {current.name} selected (burst {current.remaining:3})")
            if current.start_time is None:
                current.start_time = time

            # Amount of time this dispatch will run
            exec_time = min(quantum, current.remaining, runfor - time)

            # run, checking for arrivals at each tick
            for _ in range(exec_time):
                time += 1
                for p in processes_left[:]:
                    if p.arrival == time:
                        print(f"Time {time:3} : {p.name} arrived")
                        queue.append(p)
                        processes_left.remove(p)

            current.remaining -= exec_time

            if current.remaining > 0:
                queue.append(current)
            else:
                current.completion_time = time
                print(f"Time {time:3} : {current.name} finished")
        else:
            print(f"Time {time:3} : Idle")
            time += 1

    return processes

def main():
    if len(sys.argv) < 2:
        print("Usage: scheduler-get.py <input file>")
        sys.exit(1)
    params, processes = read_input(sys.argv[1])
    algo = params['use']
    runfor = params['runfor']

    # print header at top (show quantum if RR)
    print_header(processes, algo, params.get('quantum'))

    if algo == "fcfs":
        result = fcfs(processes, runfor)
    elif algo == "sjf":
        result = sjf_preemptive(processes, runfor)
    elif algo == "rr":
        result = round_robin(processes, runfor, params['quantum'])
    else:
        print("Error: Unknown scheduling algorithm.")
        sys.exit(1)

    print_summary(result, runfor)

if __name__ == "__main__":
    main()
