import dash
from dash import dcc, html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Mobile Price Prediction - Analysis Dashboard', style={'textAlign': 'center'}),
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
                    style={'width': '50%', 'margin': '20px auto'}
                ),
                html.Div(id='plot-container')
            ])
        ]),
        dcc.Tab(label='Price Class Prediction', children=[
            html.Div([
                html.H3('K-Nearest Neighbors Prediction'),
                dcc.Input(id='k-value', type='number', placeholder='Choose k...', min=1, max=20, value=5),
                html.Button('Predict', id='predict-button'),
                html.Div(id='prediction-results')
            ], style={'padding': '20px'})
        ])
    ])
])