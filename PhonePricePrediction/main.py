from fileRead import file_read
from model import knn_predict

# Read Dataset and create train/test sets
x_train, y_train, x_test = file_read()
# Call the model function
y_hat = knn_predict(x_train, y_train, x_test, k=45)

# Display the result
print(f"Result:\n{y_hat}")