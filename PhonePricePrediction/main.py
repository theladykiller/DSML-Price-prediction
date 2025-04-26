from HelperMethods.fileRead import file_read
from HelperMethods.printResult import print_result
from HelperMethods.DataScale import data_scale

from PlotCreation.plot import plot
from PlotCreation.classifiedPlot import classified_plot

from model import knn_predict

# Read Dataset and create train/test sets
x_train, y_train, x_test = file_read()

# Explore Data
plot(x_train, y_train)
classified_plot(x_train, y_train)

# Scale Data
x_train, x_test = data_scale(x_train, x_test)

# Call the model function
y_hat, prediction_details = knn_predict(x_train, y_train, x_test, k=45)

# Show results
print_result(y_hat, prediction_details)