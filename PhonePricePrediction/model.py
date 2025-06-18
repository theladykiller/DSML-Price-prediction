import numpy as np
import pandas as pd

def knn_predict(x_train, y_train, x_test, k):
    # Convert to numeric
    x_train = np.asarray(x_train, dtype=np.float64)
    y_train = np.asarray(y_train, dtype=np.int64)
    x_test = np.asarray(x_test, dtype=np.float64)

    # Vektorisierte Distanzberechnung für alle Testpunkte gleichzeitig
    distances = np.sqrt(((x_test[:, np.newaxis] - x_train) ** 2).sum(axis=2))
    knn_indices = np.argpartition(distances, k, axis=1)[:, :k]
    results = []
    all_details = []
    
    for i, indices in enumerate(knn_indices):
        knn_labels = y_train[indices]
        yhat = int(pd.Series(knn_labels).mode()[0])
        mean_distance = float(np.mean(distances[i, indices]))
        
        prediction_details = {
            "test_point": i+1,
            "predicted_price": yhat,
            "nearest_neighbors": indices.tolist(),
            "neighbor_labels": knn_labels.tolist(),
            "avg_distance": mean_distance
        }
        all_details.append(prediction_details)
        results.append(yhat)

    return np.array(results), all_details