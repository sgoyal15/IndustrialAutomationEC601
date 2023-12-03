import os
import numpy as np
import cv2
import json
import threading
import logging
# from config import config, get_worker_config
import time
import signal
from datetime import datetime, timedelta
from timer import total_time_taken
import csv
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from config import config, get_worker_config, hex_colors
import webbrowser 
# from stats import hex_colors
# import matplotlib.pyplot as plt

# file_path ='/Users/shivam_goyal/Desktop/ECE601/Sprint3/'

file_path =config.get('file_path')

check_file=file_path+config.get('face_data_location')

config_file_path=file_path+'config.json'

# General function to run the python file

def delete_data_at_6_am(file_path,deletion_flag_file):
    # Get the current date and time
    current_datetime = datetime.now()

    # Set the target time to 6:00 AM
    target_time_start = current_datetime.replace(hour=6, minute=0, second=0, microsecond=0)
    target_time_end = current_datetime.replace(hour=7, minute=0, second=0, microsecond=0)

    # Check if the current time is between 6 AM and 7 AM
    if target_time_start <= current_datetime <= target_time_end:
        # Check if the deletion flag file exists
        if not os.path.exists(deletion_flag_file):
            try:
                # Create the deletion flag file
                with open(deletion_flag_file, 'w'):
                    pass

                # Open the file in write mode to clear its contents
                with open(file_path, mode='w', newline=''):
                    pass  # Clear the contents of the file (since it's already open)

                print("Data cleared from the file at 6 AM.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Data already cleared between 6 AM and 7 AM.")
    # else:
    #     print("It's not between 6 AM and 7 AM.")


def load_config(file_path=config_file_path):
    try:
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Unable to decode JSON in config file '{file_path}'.")
        print(f"JSONDecodeError: {e}")
        return None

def save_config(config, file_path=config_file_path):
    try:
        with open(file_path, 'w') as config_file:
            json.dump(config, config_file, indent=2)
        print(f"Worker added successfully. Config file updated.")
    except Exception as e:
        print(f"Error: Unable to save config file '{file_path}'.")
        print(f"Exception: {e}")

def add_worker(name, shift_time, file_path=config_file_path):
    # Load the existing configuration
    config = load_config(file_path)

    if config is not None:
        # Add a new worker to the "workers" list
        new_worker = {"name": name, "shift_time": shift_time}
        config["workers"].append(new_worker)

        # Save the updated configuration
        save_config(config, file_path)


def run_file_thread():
    print("Executing file in a thread.")
    run_file(file_path)

def run_file(file_name):
    try:
        with open(file_name, 'r') as file:
            python_code = file.read()
            exec(python_code)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist. Create one!")


def is_file_present_using_os(name):
        # return os.path.isfile(check_file)
    # file_name=input("Verify the identity: ")
    # Example usage:
    file_path = check_file+ file_name +'.npy'
    # print(file_path)
    if os.path.isfile(file_path):
        return True
        
    else:
        return False

def check_data_json(name):
    path=config.get('file_path')+'config.json'
    with open(path, 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    # search_name = input("Enter a name to check if it's present in the JSON file: ")
    search_name = name
    # Check if the entered name is present in the list of workers
    name_present = any(worker["name"].lower() == search_name.lower() for worker in data.get("workers", []))
    # Print the result
    if name_present:
        return True
    else:
        return False

def execute_fingerprint_file():
    if (is_file_present_using_os()): 
        time.sleep(1)
        print("File is Present, starting the next step....")
        time.sleep(1)
        run_file(file_path+config.get('face_recog_file'))
    else:
        time.sleep(1)
        print("File is not present, data registration begins now...")
        time.sleep(1)
        run_file(file_path+config.get('face_collect_file'))
        run_file(file_path+config.get('face_recog_file'))


def save_to_csv(worker_name, time_taken):
    csv_file_path = config.get('file_path')+'output_data.csv'
    header = ['Worker Name', 'Total Taken for Task', 'Timestamp']

    # Check if the file exists, if not, write the header
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)

        # Check if worker name already exists
        worker_exists = False
        if file_exists:
            with open(csv_file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == worker_name:
                        worker_exists = True
                        break

        # If worker name exists, append a new row with updated values
        if worker_exists:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([worker_name, time_taken, timestamp])
        else:
            # If worker name does not exist, write a new row
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([worker_name, time_taken, timestamp])


def read_time_from_csv(file_path=config.get('file_path')+config.get('temp_csv')):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Assuming the CSV has only one row and one column
        time_taken = next(reader)[0]
        return time_taken

def sort_csv_alphabetically(file_path='output_data.csv'):
    # Read the CSV file and sort it alphabetically based on the first column (Worker Name)
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header
        rows = sorted(reader, key=lambda x: x[0])

    # Write the sorted data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header
        writer.writerows(rows)  # Write the sorted rows

file_executed = False

# def execute_after_delay(file_path, delay_minutes=5):
#     global file_executed
    
#     if not file_executed:
#         run_file(file_path)
#         file_executed = True
#         print("Setting file_executed to True.")
    
#     print(f"Waiting for {delay_minutes} minutes before the next execution...")
#     # time.sleep(delay_minutes * 60)  # Convert minutes to seconds
#     # print(f"Executing the file again: {file_path}")
#     # run_file(file_path)

# file_thread = threading.Thread(target=execute_after_delay, args=(file_path + config.get('fingerprint_file'),))
def realtime_graph_thread():
    while True:
        run_file(config.get('file_path')+config.get('final_stats'))

        # Check if 'quit' is pressed
        if input("Enter 'quit' to stop the real-time graph thread: ").lower() == 'quit':
            print("Stopping real-time graph thread...")
            break

def main_fun():
    selected_option = None
    
    start_time = time.time()

    while True:

        elapsed_time = time.time() - start_time
        # if elapsed_time >= 300 or selected_option is None:
        
        time.sleep(1)

        print("Choose an option:")
        time.sleep(1)
        print("1. Fingerprint Recognition")
        time.sleep(1)
        print("2. Face Recognition")
        time.sleep(1)

        selected_option = input("Enter the number(1/2) of your choice ('quit' to exit): ")
            # if selected_option.lower=='1':
            # start_time = time.time()  # Reset the timer
        # graph_thread = threading.Thread(target=realtime_graph_thread)
        # graph_thread.start()
        if selected_option.lower() == 'quit':
            print("Quiting the program......")
            time.sleep(2)
            print("Calculating the stats of the day per Workers......")
            for ix in range(5):
                print('........')
                time.sleep(1)
            run_file(config.get('file_path') + config.get('final_stats'))
            break

        elif selected_option == '1':
            
            name = input('Verify the worker name allotted to the station: ')
            time.sleep(1)
            print("Worker name is {}".format(name))

            if check_data_json(name):
                # Ask for the choice only if 5 minutes have passed or it's the first iteration
                if elapsed_time >= 300:
                    # time.sleep(1)
                    run_file(file_path + config.get('fingerprint_file'))
                    start_time = time.time()
                # file_thread.start()
                # file_thread.join()
                # execute_after_delay(file_path + config.get('fingerprint_file'))
                run_file(file_path + config.get('qrcode_file'))
                print("Going for the next step->>>>>>>")
                time.sleep(1)
                run_file(file_path + config.get('timer_file'))
                time_taken = read_time_from_csv()
                save_to_csv(name, time_taken)
            else:
                print('Adding worker {} to the json file.... '.format(name))
                add_worker(name, True)
                time.sleep(1)
                print('Worker {} added.... '.format(name))
                time.sleep(3)
                print('Fingerprint registration is starting for worker {}....'.format(name))
                for ix in range(5):
                    print('.............')
                    time.sleep(1)
                time.sleep(2)
                print('Registration is successful....')
                time.sleep(3)
                print('Authentication Required ....')
                time.sleep(1)
                run_file(file_path + config.get('fingerprint_file'))
                run_file(file_path + config.get('qrcode_file'))
                print("Going for the next step->>>>>>>")
                time.sleep(1)
                run_file(file_path + config.get('timer_file'))
                time_taken = read_time_from_csv()
                save_to_csv(name, time_taken)

        elif selected_option == '2':
            name = input('Verify the worker name allotted to the station: ')
            if check_data_json(name):
                if is_file_present_using_os(name):
                    run_file(file_path + config.get('face_recog_file'))
                else:
                    print('Worker {} facial registration is starting for station {}'.format(name, config.get('station_id')))
                    time.sleep(1)
                    run_file(file_path + config.get('face_collect_file'))
                    run_file(file_path + config.get('face_recog_file'))
            else:
                print('Worker {} will be added to the config file'.format(name))
                add_worker(name, True)
                time.sleep(1)
                print('Worker {} added successfully'.format(name))
                time.sleep(1)
                print('Worker registration is starting for station {}'.format(config.get('station_id')))
                time.sleep(1)
                run_file(file_path + config.get('face_collect_file'))
                run_file(file_path + config.get('face_recog_file'))

        else:
            print("Invalid choice. Please enter 1 or 2.")

    # graph_thread.join()
    delete_data_at_6_am(config.get('file_path')+'output_data.csv',config.get('file_path')+'delete_flag.txt')
    sort_csv_alphabetically()

if __name__ == "__main__":
    main_fun()