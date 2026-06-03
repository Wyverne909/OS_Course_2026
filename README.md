# OS_Course_2026

Nom : ALBRYCHT Paul 
Numéro d'étudiant : st64022


Assignment 2: File System Interaction Report

### 1. OS Functions and Libraries Used
For this assignment, I chose Python and utilized the built-in `os` and `stat` libraries to interact with the underlying Linux file system. 

* **`os.listdir(path)`**: I used this function to iterate through the directory. At the OS level, this acts as a wrapper around the POSIX C library functions `opendir()` and `readdir()`, allowing the program to read the directory entries.
* **`os.stat(filepath)`**: This is the core function of the script. It directly performs the `stat()` system call to the Linux kernel. It retrieves the metadata (the inode information) of the file without actually opening the file's contents.
* **`file_stats.st_size`**: Extracts the exact file size in bytes from the stat structure.
* **`stat.filemode(file_stats.st_mode)`**: The OS returns file permissions as a bitmask (integer). I used this helper function to parse that bitmask into a human-readable standard Linux format (e.g., `-rwxr-xr-x`), which clearly displays read/write/execute rights for the owner, group, and others.

### 2. Proof of Execution
*(Note for the professor: Please see the repository for the `filesystem_info.py` source code. Below is a copy of the console output when executing the script on the `sample_data` directory in a Linux environment.)*

```text
Enter a directory path (press Enter for current directory '.'): sample_data

=== Analyzing Directory: sample_data ===
File: README.md
  -> Size: 962 bytes
  -> Permissions: -rwxr-xr-x
------------------------------
File: anscombe.json
  -> Size: 1697 bytes
  -> Permissions: -rwxr-xr-x
------------------------------
File: mnist_train_small.csv
  -> Size: 36523880 bytes
  -> Permissions: -rw-r--r--
------------------------------
```

<img width="713" height="786" alt="image" src="https://github.com/user-attachments/assets/eb0141ea-304f-4638-8885-34416bc5a6a6" />
<img width="675" height="325" alt="image" src="https://github.com/user-attachments/assets/89d3245c-450f-4115-8a1e-7db870a9ab6b" />

Assignment 3: Process Creation & IPC Report

### 1. IPC Mechanism Chosen
For this task, I utilized the `multiprocessing` module in Python and chose a **Pipe** (`multiprocessing.Pipe()`) as the Inter-Process Communication (IPC) mechanism. 

**Why is it appropriate?**
A Pipe provides a two-way (duplex) communication channel between exactly two endpoints. Since this assignment strictly requires a 1-to-1 interaction (a single parent sending data to a single child, and the child replying back), a Pipe is the most efficient and straightforward choice. While a Shared Queue could also work, Queues are generally better suited for scenarios with multiple producers or multiple consumers. For direct point-to-point communication, a Pipe avoids the overhead of a Queue's internal locking mechanisms.

### 2. Proof of Execution
*(Note for the professor: Please see the repository for the `ipc_process.py` source code. Below is a copy of the console output showing proper process creation, data transformation, and clear PIDs.)*

```text
Parent [PID 1018] starting...
Child  [PID 10224] waiting for data...
Child  [PID 10224] received: 'hello operating systems'
Child  [PID 10224] transforming data to: 'SMETSYS GNITAREPO OLLEH'
Child  [PID 10224] sending data back...
Parent [PID 1018] sending data: 'hello operating systems'
Parent [PID 1018] received transformed data: 'SMETSYS GNITAREPO OLLEH'
Parent [PID 1018] finished. Child process terminated.
```

<img width="873" height="426" alt="image" src="https://github.com/user-attachments/assets/f3e21a71-5fde-43f1-9af8-ab2c82334508" />


## Assignment 4: Threads & Synchronization Report

### 1. Understanding Race Conditions (The Problem)
Based on the execution of Part 1 in my script, a **Race Condition** occurs when multiple threads access and modify a shared resource concurrently without coordination. Even though `counter += 1` looks like a single command, at the CPU level, it is actually three distinct steps: read the current value, add one, and write the new value back. 

Because the CPU rapidly switches context between the 4 threads, Thread A might read the value (e.g., 100), but before it can write 101 back, Thread B reads the same value (100). Both threads do their math and write 101 back to memory. Instead of the counter going up by 2, it only went up by 1. One increment is completely overwritten and "lost". This is why my unsynchronized counter resulted in a random, incorrect number far below the expected 4,000,000.

### 2. How Mutex/Locks Solve the Problem
In Part 2, I solved this issue by introducing a synchronization primitive: a **Lock** (Mutex), using `threading.Lock()`. 

A Mutex acts like a key to a single-occupancy room (the critical section where the shared counter is modified). When a thread reaches the `with counter_lock:` statement, it locks the door. If the other 3 threads arrive, they are forced to wait outside. The thread inside can safely read, increment, and write the variable without interruption. Once finished, it unlocks the door, allowing the next thread in line to proceed. This strict, one-at-a-time access ensures complete data integrity, which is why Part 2 successfully printed exactly 4,000,000 every single time.

### 3. Proof of Execution
*(Note for the professor: Please see the repository for the `threads_sync.py` source code. Below is the console output demonstrating the failure of the unsynchronized threads and the success of the locked threads.)*

```text
=== Part 1: Simulating a Race Condition (No Synchronization) ===
Expected Counter Value: 400000
Actual Counter Value:   100003
Difference (Lost increments): 299997

=== Part 2: Solving the Race Condition (With Mutex/Lock) ===
Expected Counter Value: 400000
Actual Counter Value:   400000
Success! The Mutex lock prevented the race condition.
```

<img width="653" height="817" alt="image" src="https://github.com/user-attachments/assets/4a476d42-6053-48b4-844a-c2d6a5355120" />
<img width="661" height="532" alt="image" src="https://github.com/user-attachments/assets/27128d1e-29d0-4e76-b1e2-bf952f395800" />

