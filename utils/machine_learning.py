import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from utils import visualization as vs
import pandas as pd


def all_model(kind_model):
    model = {"Linear Regression": LinearRegression(),
             'Logistic Regression': LogisticRegression()}

    return model[kind_model]


def linear_regression(data1, data2):
    x = np.array(data1).reshape(-1, 1)
    y = np.array(data2).reshape(-1, 1)

    regr = LinearRegression()
    regr.fit(x, y)

    score = regr.score(x, y)
    y_pred = regr.predict(x)

    return y_pred, score


def model_dbscan(data_ml, target):
    data_ml.drop(['Provinsi',
                  target], inplace=True, axis=1)

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


def supervised_learning(kind_model, data_ml, data_ml_proj, target, years, proj_years):
    X = data_ml.drop(['Provinsi',
                      target], axis=1)

    y = data_ml[target]

    X_proj = data_ml_proj.drop(['Provinsi',
                                target], axis=1)

    y_proj = data_ml_proj[target]

    # Dropping any rows with Nan values
    X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.2)

    # Splitting the data into training and testing data
    build_ml = all_model(kind_model)

    build_ml.fit(X_train, y_train)
    score = build_ml.score(X_test, y_test)

    data_predict = build_ml.predict(X_proj.values)

    data_ml_true = pd.DataFrame({'Provinsi': data_ml['Provinsi'].values,
                                 years: data_ml[target].values,
                                 proj_years: data_predict})

    chart_datas = pd.melt(data_ml_true, id_vars=["Provinsi"])

    title1 = "Efficiency Projection Each Province in " + str(years)
    title2 = "Efficiency Projection Each Province in " + str(proj_years)

    chart1 = vs.get_bar_vertical(chart_datas[chart_datas['variable'] == years],
                                 "Provinsi",
                                 "value",
                                 "variable",
                                 "Province",
                                 "Efficiency Value",
                                 title1)

    chart2 = vs.get_bar_vertical(chart_datas[chart_datas['variable'] == proj_years],
                                 "Provinsi",
                                 "value",
                                 "variable",
                                 "Province",
                                 "Efficiency Value",
                                 title2)

    return chart1, chart2, score, data_ml_true

