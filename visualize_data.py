import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

# Read the data
data = pd.read_csv("https://raw.githubusercontent.com/galihatha/Visdat/main/data-penumpang-bus-transjakarta-januari-desember-2021.csv")
data.set_index('bulan', inplace=True)

# Remove rows with NaN values in 'jenis' column
data = data.dropna(subset=['jenis'])

# Convert 'jenis' column to string
data['jenis'] = data['jenis'].astype(str)

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=data['jenis'].unique().tolist(), palette=Spectral6)

# Create the figure: plot
plot = figure(title='Data Penumpang Bus TransJakarta', x_axis_label='Jenis', y_axis_label='Kode Trayek',
              plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@trayek')])

# Add a circle glyph to the figure
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='x', transform=color_mapper), legend='jenis')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'

# Define the callback function: update_plot
def update_plot(month, x, y):
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
        'x': data[data.index == month][x],
        'y': data[data.index == month][y],
        'trayek': data[data.index == month]['trayek'],
        'jumlah_penumpang': data[data.index == month]['jumlah_penumpang']
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'Data Penumpang Bus TransJakarta - Bulan %s' % month

# Create layout
st.title("Data Penumpang Bus TransJakarta")
month = st.slider("Bulan", min_value=1, max_value=12, step=1, value=1)
x_select = st.selectbox("x-axis data", options=['jenis', 'kode_trayek', 'trayek', 'jumlah_penumpang'], index=0)
y_select = st.selectbox("y-axis data", options=['jenis', 'kode_trayek', 'trayek', 'jumlah_penumpang'], index=1)

update_plot(month, x_select, y_select)

# Add the plot to Streamlit app
st.bokeh_chart(plot)
