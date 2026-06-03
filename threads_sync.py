import threading
import time

counter_unsync = 0
counter_sync = 0
ITERATIONS = 100000
NUM_THREADS = 4

def increment_without_lock():
    global counter_unsync
    for _ in range(ITERATIONS):
        temp = counter_unsync

        time.sleep(0) 

        counter_unsync = temp + 1

counter_lock = threading.Lock()

def increment_with_lock():
    global counter_sync
    for _ in range(ITERATIONS):
        with counter_lock:
            temp = counter_sync
            time.sleep(0)
            counter_sync = temp + 1

if __name__ == "__main__":
    expected_total = ITERATIONS * NUM_THREADS

    print("=== Part 1: Simulating a Race Condition (No Synchronization) ===")
    threads_unsync = []
    
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=increment_without_lock)
        threads_unsync.append(t)
        t.start()
    
    for t in threads_unsync:
        t.join()
        
    print(f"Expected Counter Value: {expected_total}")
    print(f"Actual Counter Value:   {counter_unsync}")
    print(f"Difference (Lost increments): {expected_total - counter_unsync}\n")

    print("=== Part 2: Solving the Race Condition (With Mutex/Lock) ===")
    threads_sync = []
    
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=increment_with_lock)
        threads_sync.append(t)
        t.start()
        
    for t in threads_sync:
        t.join()
        
    print(f"Expected Counter Value: {expected_total}")
    print(f"Actual Counter Value:   {counter_sync}")
    if counter_sync == expected_total:
        print("Success! The Mutex lock prevented the race condition.")


