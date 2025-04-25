import numpy as np
import pandas as pd

def knn_predict(x_train, y_train, x_test, k):
    results = []
    all_details = []

    for i, tp in enumerate(x_test):
        # Calculate Manhattan distance to all training points
        distances = np.sum(np.abs(x_train - tp), axis=1)

        knn_indices = np.argsort(distances)[:k]

        # labels of k-nearest neighbors
        knn_labels = y_train[knn_indices]

        # Find the most frequent class
        yhat = int(pd.Series(knn_labels).mode()[0])

        # Compute mean Manhattan distance of neighbors
        mean_distance = float(np.mean(distances[knn_indices]))

        # Store all details for this prediction
        prediction_details = {
            "test_point": i,
            "predicted_price": yhat,
            "nearest_neighbors": knn_indices.tolist(),
            "neighbor_labels": knn_labels.tolist(),
            "avg_distance": mean_distance
        }
        all_details.append(prediction_details)
        results.append(yhat)

    return np.array(results), all_details
