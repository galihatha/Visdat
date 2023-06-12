import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

# Load the data
data = pd.read_csv("https://raw.githubusercontent.com/galihatha/Visdat/main/data-penumpang-bus-transjakarta-januari-desember-2021.csv")
data.set_index('bulan', inplace=True)
data = data.dropna(subset=['jenis'])
data['jenis'] = data['jenis'].astype(str)

# Make a color mapper
color_mapper = CategoricalColorMapper(factors=data['jenis'].unique().tolist(), palette=Spectral6)

# Create the figure
plot = figure(title='Data Penumpang Bus TransJakarta', x_axis_label='Jenis', y_axis_label='Kode Trayek',
              plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@trayek')])

# Add a circle glyph to the figure
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='x', transform=color_mapper), legend='jenis')

# Define the update_plot function
def update_plot(month, x, y):
    # Filter the data based on the selected month
    filtered_data = data[data.index == month]
    
    # Create a new data source
    source = ColumnDataSource(data={
        'x': filtered_data[x],
        'y': filtered_data[y],
        'trayek': filtered_data['trayek'],
        'jumlah_penumpang': filtered_data['jumlah_penumpang']
    })
    
    # Update the plot with the new data
    plot.title.text = 'Data Penumpang Bus TransJakarta - Bulan %s' % month
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    plot.source = source

# Create the Streamlit app
def main():
    st.title('Data Penumpang Bus TransJakarta')
    
    # Create the slider for selecting the month
    month = st.slider('Bulan', 1, 12, 1)
    
    # Create the dropdown menus for selecting x and y axis
    x = st.selectbox('x-axis data', ['jenis', 'kode_trayek', 'trayek', 'jumlah_penumpang'])
    y = st.selectbox('y-axis data', ['jenis', 'kode_trayek', 'trayek', 'jumlah_penumpang'])
    
    # Update the plot when the inputs are changed
    update_plot(month, x, y)
    
    # Render the plot
    st.bokeh_chart(plot)

if __name__ == '__main__':
    main()
