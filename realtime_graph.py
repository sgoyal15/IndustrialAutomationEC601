import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from config import config, get_worker_config

CSV_FILE = config.get('file_path') + config.get('temp_csv')

counter = count()
message = ''

def read_csv():
    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                time = float(row[0])
                iteration = next(counter)

            return time, iteration
    except (FileNotFoundError, ValueError, IndexError):
        return None, None

def update(frame):
    global message
    time, iteration = read_csv()
    if time is not None and iteration is not None:
        x_values.append(iteration)
        y_values.append(time)

        # Change line color based on y-axis value
        if time <= 10:
            line_color = 'green'
        elif 10 < time <= 15:
            line_color = 'orange'
        else:
            line_color = 'red'

        line.set_data(x_values, y_values)
        line.set_color(line_color)

        # Clear previous text
        for text in ax.texts:
            text.set_text('')

        if line_color == 'green':
            message = 'Good Job...'
            text_color = 'green'
        elif line_color == 'orange':
            message = 'Try to finish faster....'
            text_color = 'orange'
        else:
            message = 'Pick up the pace...'
            text_color = 'red'

        ax.text(0.95, 0.9, message, transform=ax.transAxes, color=text_color, ha='right', va='center')

    return line,

# Initialize empty lists to store x and y-axis values
x_values = []
y_values = []

# Set up the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_ylim(0, 50)
ax.set_xlim(0, 100)
# ax.legend()
ax.set_title("Efficiency Stats")
# Set up the animation with cache_frame_data=False and save_count=MAX_FRAMES
ani = FuncAnimation(fig, update, frames=None, interval=2000, cache_frame_data=False, save_count=50)
# plt.get_current_fig_manager().window.setGeometry(100, 100, 800, 600)
# Show the plot
plt.show()
