import numpy as np
from tabulate import tabulate

def printResult(y_hat, prediction_details):
    # list of rows for the table
    table_data = []
    for idx, (price, details) in enumerate(zip(y_hat, prediction_details), 1):
        table_data.append([
            idx,
            f"${price:,.2f}",
            f"{details['avg_distance']:.3f}",
            len(set(details['neighbor_labels']))  # Number of unique labels
        ])

    # Print header
    print("\n" + "=" * 80)
    print(" PHONE PRICE PREDICTION - DETAILED RESULTS ".center(80))
    print("=" * 80 + "\n")

    # Print main table using tabulate
    print(tabulate(
        table_data,
        headers=["No.", "Predicted Price", "Avg Distance", "Unique Classes"],
        tablefmt="pretty",
        numalign="right"
    ))

    # Print detailed statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS".center(80))
    print("=" * 80)
    print(f"Number of predictions: {len(y_hat)}".center(80))
    print(f"Average predicted price: ${np.mean(y_hat):,.2f}".center(80))
    print(f"Average distance to neighbors: {np.mean([d['avg_distance'] for d in prediction_details]):.3f}".center(80))

    # Print detailed information for each prediction
    print("\n" + "=" * 80)
    print("DETAILED INFORMATION FOR EACH PREDICTION".center(80))
    print("=" * 80)

    for details in prediction_details:
        print(f"\nTest Point [{details['test_point']}]:")
        print(f"  Predicted Price: ${details['predicted_price']:,.2f}")
        print(f"  Average Distance: {details['avg_distance']:.3f}")
        print(f"  Nearest Neighbor Indices: {details['nearest_neighbors']}")
        print(f"  Neighbor Labels: {details['neighbor_labels']}")
        print("-" * 80)
