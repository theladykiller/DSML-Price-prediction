import pandas as pd
import numpy as np

def knn_predict(x_train, y_train, x_test, k):
    results = []

    for i, tp in enumerate(x_test):
        print(f"TestPoint[{i}]:")
        # Calculate Manhattan distance to all training points
        # Calculate difference for all columns
        # Take the positive value
        # Sum differences of all columns
        # Do this 1000 times for each X_train point
        distances = np.sum(np.abs(x_train - tp), axis=1)
        #print(f"Amount of distances(comparisons between the Test point and all X_training sets): {distances.size}")
        #print(f"{distances}")

        # Get indices of k smallest distances
        # Sort the distances in ascending order
        # Return 5 smallest indices (Indices of the 5-nearest-neighbors to the Test Point)
        knn_indices = np.argsort(distances)[:k]
        print(f"Indices for the k={k} smallest distances = {knn_indices}")

        # Get class labels of k-nearest neighbors
        # Use those 5 smallest indices (knn_indices) to find the "class" values inside y_train
        knn_labels = y_train[knn_indices]
        print(f"Labels for the k={k} smallest distances:\n{knn_labels}")

        # Find the most frequent class (mode)
        # Convert labels to pandas Series
        # Return most frequent value as int
        # mode() returns the most frequent value multiple times
        # Use [0] to just get the first in the list
        yhat = int(pd.Series(knn_labels).mode()[0])
        print(f"Most frequent label = {yhat}")

        # Compute mean Manhattan distance of neighbors
        # Take the distances at the given indices (distances of the 5 closest neighbors)
        # Sum distances and divide by amount of distances (average distance)
        mean_distance = float(np.mean(distances[knn_indices]))
        print(f"Average distance to {k} nearest neighbors = {round(mean_distance, 3)}\n")

        # Convert indices to a string
        idx_str = str([int(i) for i in knn_indices])
        # Append result
        # yhat = predicted class
        # mean_distance = average distance to 5-nearest neighbors
        # idx_str = indices of 5 nearest neighbors from X_train
        results.append([yhat, mean_distance, idx_str])

    # Return DataFrame
    return pd.DataFrame(results, columns=["yhat", "mndist", "idx"])