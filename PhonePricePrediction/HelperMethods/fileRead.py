import pandas as pd

from pathlib import Path

def file_read():
    # Declare data directory
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"

    # Load the CSV files
    train_df = pd.read_csv(data_dir / 'train.csv', sep=',')
    test_df = pd.read_csv(data_dir / 'test.csv', sep=',')

    # Split data
    x_train = train_df.drop(columns=["price_range"])
    y_train = train_df["price_range"]  # Values 0, 1, 2, 3
    x_test = test_df.drop(columns=["id"])

    # Rename columns
    rename_conditions = {
        'battery_power': 'Battery Power',
        'blue': 'Bluetooth',
        'clock_speed': 'Processor Clock Speed',
        'dual_sim': 'Dual Sim',
        'fc': 'Front Camera Mega Pixels',
        'four_g': '4G',
        'int_memory': 'Storage Capacity',
        'm_dep': 'Phone Depth',
        'mobile_wt': 'Weight',
        'n_cores': 'Processor Cores',
        'pc': 'Primary Camera Mega Pixels',
        'px_height': 'Resolution Height',
        'px_width': 'Resolution Width',
        'ram': 'RAM',
        'sc_h': 'Screen Height',
        'sc_w': 'Screen Width',
        'talk_time': 'Battery Duration',
        'three_g': '3G',
        'touch_screen': 'Touch Screen',
        'wifi': 'WIFI'
    }
    x_train.rename(columns=rename_conditions, inplace=True)
    x_test.rename(columns=rename_conditions, inplace=True)
    y_train.name = 'Price Range'

    return x_train, y_train, x_test