from sklearn.preprocessing import MinMaxScaler

def data_scale(x_train_unscaled, x_test_unscaled):
    mmSc = MinMaxScaler()
    x_train = mmSc.fit_transform(x_train_unscaled)
    x_test = mmSc.fit_transform(x_test_unscaled)

    return x_train, x_test