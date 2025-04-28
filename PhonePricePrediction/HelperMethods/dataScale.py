from sklearn.preprocessing import MinMaxScaler

def data_scale(x_train_unscaled, x_test_unscaled):
    mmSc = MinMaxScaler()
    x_train = mmSc.fit_transform(x_train_unscaled)
    x_test = mmSc.transform(x_test_unscaled) #hier statt fit_transform nur transform
    return x_train, x_test

"""
Das fit_transform sollte nur auf den Trainingsdaten ausgeführt werden, für die Testdaten nur transform
Erklärung:
fit_transform(X_train) = Der Scaler lernt Minimum und Maximum aus den Trainingsdaten und skaliert sie.
transform(X_test) = Der Scaler wendet dieselbe Skalierung auf die Testdaten an (ohne neu zu lernen).
"""