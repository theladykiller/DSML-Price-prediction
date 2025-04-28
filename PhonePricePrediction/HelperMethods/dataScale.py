from sklearn.preprocessing import MinMaxScaler

def data_scale(x_train_unscaled, x_test_unscaled):
    misc = MinMaxScaler()
    x_train = misc.fit_transform(x_train_unscaled)
    x_test = misc.transform(x_test_unscaled)

    return x_train, x_test