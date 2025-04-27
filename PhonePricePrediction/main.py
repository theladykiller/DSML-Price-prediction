from PhonePricePrediction.HelperMethods.fileRead import file_read
from PhonePricePrediction.HelperMethods.printResult import print_result
from PhonePricePrediction.HelperMethods.DataScale import data_scale

from PlotCreation.regressionCurvePlot import regression_curve_plot
from PlotCreation.highToLowEndPlot import low_to_high_end_plot
from PlotCreation.barPlot import bar_plot

from model import knn_predict

# Read Dataset and create train/test sets
x_train, y_train, x_test = file_read()

# Explore Data
bar_plot(x_train, y_train)
regression_curve_plot(x_train, y_train)

# Scale Data
x_train, x_test = data_scale(x_train, x_test)

# Further Data Exploration
low_to_high_end_plot(x_train, y_train)

# Call the model function
y_hat, prediction_details = knn_predict(x_train, y_train, x_test, k=45)

# Show results
print_result(y_hat, prediction_details)