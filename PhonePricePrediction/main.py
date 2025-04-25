
from fileRead import file_read
from model import knn_predict
from printResult import print_result

# Read Dataset and create train/test sets
x_train, y_train, x_test = file_read()
# Call the model function
y_hat, prediction_details = knn_predict(x_train, y_train, x_test, k=45)
# Show results
print_result(y_hat, prediction_details)