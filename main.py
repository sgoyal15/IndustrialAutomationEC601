import os
import numpy as np
file_path ='/Users/shivam_goyal/Desktop/ECE601/Sprint3/'

check_file=file_path+'faceDataCollect/'

# General function to run the python file
def run_file(file_name):
    try:
        with open(file_name, 'r') as file:
            python_code = file.read()
            exec(python_code)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist. Create one!")


def is_file_present_using_os():
        # return os.path.isfile(check_file)
    file_name=input("Checking data for person: ")
    # Example usage:
    file_path = check_file+ file_name +'.npy'
    # print(file_path)
    if os.path.isfile(file_path):
        return True
        # print(f"The file '{file_path}' is present.")
    else:
        return False
        # print(f"The file '{file_path}' is not present.")

# Check whether user data is present or not!

def execute_python_file(file_path):
    if (is_file_present_using_os()): 
        print("File is Present")
       # try:
       #    with open(file_path+'face_recognision.py', 'r') as file:
       #       python_code = file.read()
       #       exec(python_code)
       # except FileNotFoundError:
       #    print(f"Error: The file '{file_path}' does not exist.")

       run_file(file_path+'face_recognision.py')
    else:
        # with open(file_path+'face_data_collect.py', 'r') as file:
        #      python_code = file.read()
        #      exec(python_code)
        # with open(file_path+'face_recognision.py', 'r') as file:
        #      python_code = file.read()
        #      exec(python_code)

        run_file(file_path+'face_data_collect.py')
        run_file(file_path+'face_recognision.py')
        # print("File is not Present")


def main():
    print("Choose an option:")
    print("1. Fingerprint Recognition")
    print("2. Face Recognition")

    choice = input("Enter the number of your choice: ")

    if choice == '1':
        with open(file_path+'fingerprintSimulate.py', 'r') as file:
             python_code = file.read()
             exec(python_code)

        run_file(file_path+'qrCode.py')

    elif choice == '2':
        execute_python_file(file_path)

    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()