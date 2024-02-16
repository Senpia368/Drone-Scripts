import time

def stopwatch():
    input("Press Enter to start the stopwatch...")
    start_time = time.time()
    print("Stopwatch started!")

    input("Press Enter to stop the stopwatch...")
    end_time = time.time()
    print("Stopwatch stopped!")

    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")

# Start the stopwatch
stopwatch()
