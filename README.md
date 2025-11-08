# Process Scheduler (FIFO, Pre-emptive SJF, and Round Robin)

This project simulates three classical CPU scheduling algorithms — **First In, First Out (FIFO)**, **Pre-emptive Shortest Job First (SJF)**, and **Round Robin (RR)** — in Python.  
It reads process definitions from an input file, simulates execution according to the selected algorithm, and outputs detailed results including process events, wait time, turnaround time, and response time.

This implementation was developed collaboratively with **ChatGPT** as part of a class project exploring AI-assisted software development.

---

## Features

- Implements three scheduling algorithms:
  - **FIFO (First In, First Out)** — non-preemptive  
  - **Pre-emptive SJF (Shortest Job First)** — dynamically selects the shortest remaining job  
  - **Round Robin (RR)** — uses a fixed quantum time slice  

- Calculates:
  - **Turnaround Time** (completion − arrival)  
  - **Waiting Time** (turnaround − burst)  
  - **Response Time** (first run − arrival)

- Handles:
  - Process arrivals and completions  
  - Idle CPU time  
  - Incomplete processes if the runtime expires  
  - Error checking for missing or malformed parameters  
  - File-based input and output  

---


**Directives:**

| Directive | Description |
|------------|--------------|
| `processcount` | Total number of processes |
| `runfor` | Total simulation time (in time units) |
| `use` | Scheduling algorithm (`fcfs`, `sjf`, `rr`) |
| `quantum` | Time slice (required only for `rr`) |
| `process` | Defines each process with name, arrival time, and burst |
| `end` | Marks the end of input |

**Error Handling:**
- Missing parameters trigger messages like:  
  `Error: Missing parameter <parameter>`  
- Missing `quantum` for Round Robin:  
  `Error: Missing quantum parameter when use is 'rr'`  
- No input file provided:  
  `Usage: scheduler-gpt.py <input file>`

---

### Output Format

The program writes results to an `.out` file using the same base name as the input.

**Example Output:**
3 processes
Using preemptive Shortest Job First

Time 0 : A arrived
Time 0 : A selected (burst 5)
Time 1 : B arrived
Time 4 : C arrived
Time 5 : A finished
Time 5 : C selected (burst 2)
Time 7 : C finished
Time 7 : B selected (burst 4)
Time 11 : B finished
Time 11 : Idle
...
Finished at time 20

A wait 0 turnaround 5 response 0
B wait 6 turnaround 10 response 6
C wait 1 turnaround 3 response 1


---

## How to Run

### Requirements
- Python 3.7+
- Command line access (Mac, Linux, or Windows)


---

## Algorithms Overview

### 1. FIFO (First In, First Out)
- Non-preemptive  
- Processes are executed in order of arrival.  
- Simple but can perform poorly with long jobs.  

### 2. Pre-emptive SJF (Shortest Job First)
- Also known as **Shortest Remaining Time First (SRTF)**.  
- Chooses the process with the smallest remaining burst time.  
- Minimizes average waiting time but requires burst time knowledge.  

### 3. Round Robin
- Time-shared scheduling algorithm.  
- Each process runs for a maximum of `quantum` time units before being preempted.  
- Fair and suitable for time-sharing systems.  

---

## Metrics Explained

| Metric | Formula | Meaning |
|---------|----------|---------|
| **Turnaround Time (TAT)** | `finish_time - arrival_time` | Total time from arrival to completion |
| **Waiting Time (WT)** | `turnaround_time - burst_time` | Time spent waiting in the ready queue |
| **Response Time (RT)** | `first_execution_time - arrival_time` | Time from arrival to first execution |

---

## AI Collaboration

This project was developed with **ChatGPT (OpenAI)** as part of an assignment on AI-assisted programming.  
Each team member contributed by crafting and refining prompts to iteratively generate the scheduling logic and format the output correctly.  

Human-written contributions are limited to:
- Minor debugging and formatting adjustments  
- Input/output validation  
- Integration of AI-generated algorithm implementations  

All human edits are commented and documented within the source file.

---

## Evaluation Criteria

| Category | Description |
|-----------|--------------|
| **Correctness** | Produces accurate results matching benchmark outputs |
| **Efficiency** | Avoids redundant operations and unnecessary loops |
| **Readability** | Clean code, clear function names, and structured flow |
| **Completeness** | Handles edge cases and malformed inputs gracefully |
| **Innovation** | Demonstrates effective use of AI-assisted development |

---

## Authors
- **Leysha Anténor**  

Course: *Operating Systems — Process Scheduling Project*  

--- 
