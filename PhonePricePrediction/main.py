import dash

from dash import dcc, html
from dash.dependencies import Input, Output, State

from PhonePricePrediction.HelperMethods.fileRead import file_read
from PhonePricePrediction.HelperMethods.dataScale import data_scale

from PhonePricePrediction.PlotCreation.constants import cost_labels, cost_categories,palette
from PhonePricePrediction.PlotCreation.barPlot import bar_plot
from PhonePricePrediction.PlotCreation.regressionCurvePlot import regression_curve_plot
from PhonePricePrediction.PlotCreation.highToLowEndPlot import low_to_high_end_plot

from PhonePricePrediction.model import knn_predict

x_train, y_train, x_test = file_read()

# Convert to numeric
x_train = x_train.astype(float)
y_train = y_train.astype(int)
x_test = x_test.astype(float)

# Scale
x_train_scaled, x_test_scaled = data_scale(x_train, x_test)

app = dash.Dash(__name__)

# Load Web Page
app.layout = html.Div([
    # Header
    html.H1('Mobile Price Prediction - Analysis Dashboard', style={'textAlign': 'center'}),
    # Tabs for different analyses
    dcc.Tabs([
        # Tab 1: Plots
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
        # Tab 2: KNN Prediction
        dcc.Tab(label='Price Class Prediction', children=[
            html.Div([
                html.H3('K-Nearest Neighbors Prediction'),
                dcc.Input(
                    id='k-value',
                    type='number',
                    placeholder='Choose k...',
                    min=1,
                    max=20,
                    value=5
                ),
                html.Button('Predict', id='predict-button'),
                html.Div(id='prediction-results')
            ], style={'padding': '20px'})
        ])
    ])
])

# Plotting Functions
@app.callback(
    Output('plot-container', 'children'),
    [Input('plot-type', 'value')]
)
def update_plots(plot_type):
    # Define Plots
    plot_functions = {
        'bar': bar_plot,
        'regression': regression_curve_plot,
        'highlow': low_to_high_end_plot
    }
    # Conditions
    if plot_type == 'highlow':
        figures = plot_functions[plot_type](x_train_scaled, y_train, use_plotly=True)
    else:
        figures = plot_functions[plot_type](x_train, y_train, use_plotly=True)
    # Return Plots
    return [dcc.Graph(figure=fig) for fig in figures]

# KNN Prediction Function
@app.callback(
    Output('prediction-results', 'children'),
    [Input('predict-button', 'n_clicks')],
    [State('k-value', 'value')]
)
def make_predictions(n_clicks, k):
    # Return for empty user input
    if n_clicks is None or k is None:
        return ''
    # Predict KNN and return as HTML
    try:
        predictions, details = knn_predict(x_train_scaled, y_train, x_test_scaled, k)
        prediction_list = [
            html.P(f"Test point {d['test_point']}: {cost_labels[d['predicted_price']]} "
                   f"(Average distance: {d['avg_distance']:.2f})")
            for d in details[:1000]
        ]
        return html.Div([
            html.H4(f'Predictions with k={k}'),
            html.Div(prediction_list)
        ])
    except Exception as e:
        return html.Div([
            html.H4('Error occurred during prediction'),
            html.P(str(e))
        ])

if __name__ == '__main__':
    app.run(debug=True)  # dev_tools_props_check=True