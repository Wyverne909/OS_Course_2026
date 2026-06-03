import multiprocessing
import os

def child_process(conn):
    """Function executed by the child process."""
    child_pid = os.getpid()
    
    print(f"Child  [PID {child_pid}] waiting for data...")
    received_data = conn.recv()
    print(f"Child  [PID {child_pid}] received: '{received_data}'")
    
    transformed_data = received_data.upper()[::-1]
    print(f"Child  [PID {child_pid}] transforming data to: '{transformed_data}'")
    
    print(f"Child  [PID {child_pid}] sending data back...")
    conn.send(transformed_data)
    
    conn.close()

if __name__ == "__main__":
    parent_pid = os.getpid()
    print(f"Parent [PID {parent_pid}] starting...")

    parent_conn, child_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=child_process, args=(child_conn,))
    
    p.start()

    original_string = "hello operating systems"

    print(f"Parent [PID {parent_pid}] sending data: '{original_string}'")
    parent_conn.send(original_string)

    response = parent_conn.recv()
    print(f"Parent [PID {parent_pid}] received transformed data: '{response}'")

    p.join()
    print(f"Parent [PID {parent_pid}] finished. Child process terminated.")

