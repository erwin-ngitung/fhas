import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA


def linear_regression(data1, data2):
    x = np.array(data1).reshape(-1, 1)
    y = np.array(data2).reshape(-1, 1)

    regr = LinearRegression()
    regr.fit(x, y)

    score = regr.score(x, y)
    y_pred = regr.predict(x)

    return y_pred, score


def model_tsne(data_ml, target):
    data_ml.drop(['Provinsi'], inplace=True)

    # Defining Model
    model = TSNE(learning_rate=100)

    # Fitting Model
    transformed = model.fit_transform(data_ml.values)

    # Plotting 2d t-Sne
    x_axis = transformed[:, 0]
    y_axis = transformed[:, 1]

    fig, ax = plt.subplots(1, figsize=(12, 10))
    ax.scatter(x_axis, y_axis, c=data_ml[target])

    return fig, ax


def model_dbscan(data_ml, target):
    data_ml.drop(['Provinsi'], inplace=True, axis=1)

    # Declaring Model
    dbscan = DBSCAN()

    # Fitting
    dbscan.fit(data_ml)

    # Transforming Using PCA
    pca = PCA(n_components=3).fit(data_ml.values)
    pca_2d = pca.transform(data_ml.values)

    fig, ax = plt.subplots(1, figsize=(10, 8))

    # Plot based on Class
    for i in range(0, pca_2d.shape[0]):
        if dbscan.labels_[i] == 0:
            c1 = ax.scatter(pca_2d[i, 0], pca_2d[i, 1], c='r', marker='+')
        elif dbscan.labels_[i] == 1:
            c2 = ax.scatter(pca_2d[i, 0], pca_2d[i, 1], c='g', marker='o')
        elif dbscan.labels_[i] == 2:
            c3 = ax.scatter(pca_2d[i, 0], pca_2d[i, 1], c='y', marker='-')
        elif dbscan.labels_[i] == -1:
            c4 = ax.scatter(pca_2d[i, 0], pca_2d[i, 1], c='b', marker='*')

    # ax.legend()
    ax.set_title('DBSCAN finds 3 clusters and Noise')

    return fig, ax, dbscan.labels_
