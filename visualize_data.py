import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

data = pd.read_csv("https://raw.githubusercontent.com/galihatha/Visdat/main/data-penumpang-bus-transjakarta-januari-desember-2021.csv")
data.set_index('bulan', inplace=True)
data = data.dropna(subset=['jenis'])
data['jenis'] = data['jenis'].astype(str)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Data Penumpang Bus TransJakarta'),
    dcc.Slider(
        id='month-slider',
        min=1,
        max=12,
        step=1,
        value=1,
        marks={str(month): str(month) for month in range(1, 13)},
        included=False
    ),
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[
            {'label': 'Jenis', 'value': 'jenis'},
            {'label': 'Kode Trayek', 'value': 'kode_trayek'},
            {'label': 'Trayek', 'value': 'trayek'},
            {'label': 'Jumlah Penumpang', 'value': 'jumlah_penumpang'}
        ],
        value='jenis',
        clearable=False
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[
            {'label': 'Jenis', 'value': 'jenis'},
            {'label': 'Kode Trayek', 'value': 'kode_trayek'},
            {'label': 'Trayek', 'value': 'trayek'},
            {'label': 'Jumlah Penumpang', 'value': 'jumlah_penumpang'}
        ],
        value='kode_trayek',
        clearable=False
    ),
    dcc.Graph(id='plot')
])

@app.callback(
    Output('plot', 'figure'),
    [Input('month-slider', 'value'),
     Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_plot(month, x, y):
    fig = make_subplots()
    filtered_data = data[data.index == month]
    fig.add_trace(go.Scatter(x=filtered_data[x], y=filtered_data[y], mode='markers'))
    fig.update_layout(
        title='Data Penumpang Bus TransJakarta - Bulan {}'.format(month),
        xaxis_title=x,
        yaxis_title=y
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

