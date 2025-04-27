from pathlib import Path

import pandas as pd

def file_read():
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"

    # Load the CSV files
    train_df = pd.read_csv(data_dir / 'train.csv', sep=',')
    test_df = pd.read_csv(data_dir / 'test.csv', sep=',')

    # Split data
    x_train = train_df.drop(columns=["price_range"])
    y_train = train_df["price_range"]  # Values 0, 1, 2, 3
    x_test = test_df.drop(columns=["id"])

    return x_train, y_train, x_test