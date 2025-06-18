from dash import dcc
from dash.dependencies import Input, Output
from app import app
from HelperMethods.fileRead import file_read
from HelperMethods.dataScale import data_scale
from PlotCreation.barPlot import bar_plot
from PlotCreation.regressionCurvePlot import regression_curve_plot
from PlotCreation.highToLowEndPlot import low_to_high_end_plot

x_train, y_train, x_test = file_read()
x_train = x_train.astype(float)
y_train = y_train.astype(int)
x_test = x_test.astype(float)
x_train_scaled, x_test_scaled = data_scale(x_train, x_test)

# Cache Plots
plot_cache = {}

@app.callback(
    Output('plot-container', 'children'),
    [Input('plot-type', 'value')]
)
def update_plots(plot_type):
    # Check cache
    if plot_type in plot_cache:
        return plot_cache[plot_type]
        
    plot_functions = {
        'bar': bar_plot,
        'regression': regression_curve_plot,
        'highlow': low_to_high_end_plot
    }

    #Select the correct data
    data = x_train_scaled if plot_type == 'highlow' else x_train
    
    # Plot-Generate
    figures = plot_functions[plot_type](data, y_train, use_plotly=True)
    result = [dcc.Graph(figure=fig) for fig in figures]

    plot_cache[plot_type] = result

    return result