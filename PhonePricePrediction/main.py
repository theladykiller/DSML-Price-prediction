from HelperMethods.fileRead import file_read
from HelperMethods.printResult import print_result
from HelperMethods.DataScale import data_scale

from DiagramCreation.diagram import diagram
from DiagramCreation.classifiedDiagram import classified_diagram

from model import knn_predict

# Read Dataset and create train/test sets
x_train, y_train, x_test = file_read()

# Explore Data
#diagram(x_train, y_train)
classified_diagram(x_train, y_train)

# Scale Data
#x_train, x_test = data_scale(x_train, x_test)

# Call the model function
#y_hat, prediction_details = knn_predict(x_train, y_train, x_test, k=45)

# Show results
#print_result(y_hat, prediction_details)