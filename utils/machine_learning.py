import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def linear_regression(data1, data2):
    x = np.array(data1).reshape(-1, 1)
    y = np.array(data2).reshape(-1, 1)

    regr = LinearRegression()
    regr.fit(x, y)

    score = regr.score(x, y)
    y_pred = regr.predict(x)

    return y_pred, score

