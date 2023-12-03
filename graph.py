import time
import os
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from datetime import datetime

def show_seconds():
    try:
        times = []  # List to store the timestamp for each iteration
        elapsed_times = []  # List to store the elapsed time for each iteration

        print("Timer Started...")

        while True:
            current_time = time.time()

            # Append the timestamp and elapsed time to the lists
            times.append(datetime.now())
            elapsed_times.append(current_time)

            # Plot the real-time graph
            plt.plot(times, elapsed_times, marker='o', linestyle='-', color='b')
            plt.xlabel("Time")
            plt.ylabel("Elapsed Time (s)")
            plt.title("Real-Time Elapsed Time Graph")
            plt.pause(1)  # Pause for 1 second to update the graph

            # Clear the plot for the next iteration
            plt.clf()

            # Check for user input
            user_input = input("Press '0' to scan QR code (or press Enter to continue): ")

            if user_input == '0':
                # Trigger the execution of qrCode.py
                os.system("python3 qrCode.py")

    except KeyboardInterrupt:
        print("\nProgram terminated.")

if __name__ == "__main__":
    show_seconds()