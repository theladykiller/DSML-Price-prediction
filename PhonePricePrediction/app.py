import dash
from dash import dcc, html

app = dash.Dash(__name__)

# Vorberechne Dropdown-Optionen
plot_options = [
    {'label': 'Feature Distribution', 'value': 'bar'},
    {'label': 'Feature-Price Regression', 'value': 'regression'},
    {'label': 'Low-End to High-End Analyze', 'value': 'highlow'}
]

app.layout = html.Div([
    html.H1('Mobile Price Prediction - Analysis Dashboard', style={
        'textAlign': 'center',
        'color': 'black',
        'marginTop': '30px',
        'fontFamily': 'Segoe UI, Arial, sans-serif'
    }),
    dcc.Tabs([
        dcc.Tab(label='Plots', children=[
            html.Div([
                dcc.Dropdown(
                    id='plot-type',
                    options=[
                        {'label': 'Feature Distribution', 'value': 'bar'},
                        {'label': 'Feature-Price Regression', 'value': 'regression'},
                        {'label': 'Low-End to High-End Analyze', 'value': 'highlow'}
                    ],
                    value='bar',
                    style={'width': '60%', 'margin': '20px auto', 'fontSize': '18px'}
                ),
                html.Div(id='plot-container', style={'margin': '30px'})
            ], style={'backgroundColor': '#0c7d94', 'padding': '30px', 'borderRadius': '12px', 'boxShadow': '0 2px 8px #ccc'})
        ]),
        dcc.Tab(label='Price Class Prediction', children=[
            html.Div([
                html.H3('K-Nearest Neighbors Prediction', style={'color': '#343a40'}),
                dcc.Input(id='k-value', type='number', placeholder='Choose k...', min=1, max=20, value=5, style={'marginRight': '10px', 'fontSize': '16px'}),
                html.Button('Predict', id='predict-button', style={'backgroundColor': '#0c7d94', 'color': 'white', 'fontSize': '16px', 'border': 'none', 'borderRadius': '5px', 'padding': '8px 16px'}),
                html.Div(id='prediction-results', style={'marginTop': '20px'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '30px', 'textAlign': 'center','borderRadius': '12px', 'boxShadow': '0 2px 8px #ccc'})
        ])
    ])
], style={'backgroundColor': '#fcfcfc', 'minHeight': '100vh'})