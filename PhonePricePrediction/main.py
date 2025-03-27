from pathlib import Path
import os

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from model import knn_predict

# Get the main.py directory
current_dir = Path(__file__).resolve().parent
# Navigate to the Data folder relative to main.py
data_dir = current_dir.parent / 'Data'

# Load the CSV files
train_df = pd.read_csv(data_dir / 'train.csv', sep=',')
test_df = pd.read_csv(data_dir / 'test.csv', sep=',')

# Split data
x_train_unscaled = train_df.drop(columns=["price_range"])
y_train = train_df["price_range"] # Values 0, 1, 2, 3
x_test_unscaled = test_df.drop(columns=["id"])

# Scale
mmSc = MinMaxScaler()
x_train = mmSc.fit_transform(x_train_unscaled)
x_test = mmSc.fit_transform(x_test_unscaled)

# Call the model function
y_hat = knn_predict(x_train, y_train, x_test, k=45)

# Display the result
print(f"Result:\n{y_hat}")