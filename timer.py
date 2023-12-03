import time
import os
import csv
# from main import save_to_csv
import pandas as pd
from config import config, get_worker_config
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from config import config, get_worker_config
# from main import run_file
def run_file(file_name):
    try:
        with open(file_name, 'r') as file:
            python_code = file.read()
            exec(python_code)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist. Create one!")

def total_time_taken(total_time_int):
    # Assuming you want to overwrite the time in the CSV file
    with open(config.get('file_path') + config.get('temp_csv'), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_time_int])

def show_seconds():
    try:
            # Get the current time in HH:MM:SS format
        current_time = time.time()
        
        print("Timer Started...")

            # Print the current time with seconds
            # print(f"\rCurrent Time: {current_time}", end="\n", flush=True)
        time.sleep(1)

            # Check for user input
        user_input = input("Press '0' to scan QR code again: ")
        time.sleep(1)    
        if user_input == '0':
                # Trigger the execution of qrCode.py
            os.system("python3 qrCode.py")

        final_time=time.time()
        total_time=final_time-current_time
        total_time_int=int(final_time-current_time)
        total_time_taken(total_time_int)
        print("The total time taken is {} ========".format(total_time))
        # run_file(config.get('file_path')+'realtime_graph.py')
        return total_time

    except KeyboardInterrupt:
        print("\nProgram terminated.")


if __name__ == "__main__":
    show_seconds()
