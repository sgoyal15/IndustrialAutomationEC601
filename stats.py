# #!/usr/bin/env python3
# import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from config import config, get_worker_config
import webbrowser  # Import the webbrowser module

# Read the CSV file into a DataFrame
df = pd.read_csv(config.get('file_path') + 'output_data.csv')

# Create a color map for unique worker names with hex color codes
hex_colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#33A1FF', '#A1FF33']  # Add more colors if needed
color_map = {name: hex_colors[i % len(hex_colors)] for i, name in enumerate(df['Worker Name'].unique())}

# Reset the index to default integer index
df_reset = df.reset_index()

# Create a bar graph with color-coded data using Plotly Express
fig = px.bar(df_reset, x='index', y='Total Taken for Task', color='Worker Name', 
             labels={'Total Taken for Task': 'Total Time Taken (int)'},
             color_discrete_map=color_map, title='Total Time Taken for Each Task by Worker')

# Show the plot
# fig.show()

# Save the plot as an HTML file
html_file_path = config.get('file_path')+'final_stats.html'
fig.write_html(html_file_path)

# Open the HTML file in the default web browser
webbrowser.open('file://' + html_file_path, new=2)  # new=2 opens in a new tab, change if needed