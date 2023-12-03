
import json

hex_colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#33A1FF', '#A1FF33']

def load_config(file_path='/Users/shivam_goyal/Desktop/ECE601/Sprint3/config.json'):
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

# Load the configuration
config = load_config()

# Access individual workers
def get_worker_config(worker_name):
    workers = config.get('workers', [])
    for worker in workers:
        if worker.get('name') == worker_name:
            return worker
    print(f"Error: Worker '{worker_name}' not found. First add the worker.")
    return None
