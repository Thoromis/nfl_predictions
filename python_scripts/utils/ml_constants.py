from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
import pandas as pd
import numpy as np

# interesting tuning thoughts: https://medium.com/all-things-ai/in-depth-parameter-tuning-for-svc-758215394769

names = [
    "Baseline_best",
    "Baseline_MostFrequent",
    "NearestNeighbors",
    # "SVC",
    # "GaussianNB",
    "DecisionTree",
    "RandomForest",
    #    "NN"
]

classifiers = {
    'Baseline_Best': DummyClassifier(),
    'Baseline_MostFrequent': DummyClassifier(),
    'NearestNeighbors': KNeighborsClassifier(),
    # 'SVC': SVC(),
    # 'GaussianNB': GaussianNB(),
    'DecisionTree': DecisionTreeClassifier(),
    'RandomForest': RandomForestClassifier(),
    #    'NN': MLPClassifier()
}

params = {
    'Baseline_Best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
    'Baseline_MostFrequent': {'strategy': ['most_frequent']},
    'NearestNeighbors': {'n_neighbors': [2, 3, 4, 5, 6, 7, 8, 9, 10]},
    # 'SVC': [
    # Linear ==> better with smaller C, but in general pretty useless
    # RBF ==> better with higher C
    # Poly ==>  degree 3, higher C is better, best > 100000
    #           degree 4, same, higher C, better, slightly better than 3
    #           degree 5 same, bit worse than 4 but also not too bad
    #    {'kernel': ['rbf'], 'C': [0.001, 0.1, 10]},
    # ],
    # 'GaussianNB': {'var_smoothing': [1e-9]},
    # Decision Tree best random search:
    # min_samples_split=0.9, max_features=3, max_depth=10 (roc_auc=0.59)
    # min_samples_split=0.1, max_features=3, max_depth=40 (roc_auc=0.58)
    'DecisionTree': {
        'max_depth': [5, 10, 40],
        # Everything above 5 will basically already overfit the training data
        'min_samples_split': [0.05, 0.1, 0.15, 0.2],
        'max_features': [3, 4]
    },
    # Random forest:  best random search for RBs:
    # 5 estimators, min_samples_split=5, min_samples_leaf=2, max_depth=50
    # 6 estimators, min_samples_split=3, min_samples_leaf=3, max_depth=10
    # 6 estimators, min_samples_split=3, min_samples_leaf=3, max_depth=5 (roc_auc=0.63)
    # 20 estimators, min_samples_split=7, min_samples_leaf=2, max_depth=5 (roc_auc=0.63)
    # 15 estimators, min_samples_split=3, min_samples_leaf=3, max_depth=80 (roc_auc=0.58)
    'RandomForest': {'max_depth': [5, 10, 15, 20, 25],
                     'n_estimators': [5, 6, 20],
                     'min_samples_split': [3],
                     'min_samples_leaf': [3]
                     },
    # 'NN': {
    #     'learning_rate': ['constant', 'invscaling', 'adaptive'],
    #     'hidden_layer_sizes': [(128,), (256,)],
    #     'shuffle': [True],
    #     'activation': ['relu'],
    #     'batch_size': [16, 64, 128],
    #     'early_stopping': [True],
    #     'max_iter': [200]
    # },
}


def persist_train_test_split(x_train, x_test, y_train, y_test, player_names_train, player_names_test, unit_key):
    x_train.to_csv('../processed_data/' + unit_key + '/train_test_splits/x_train.csv')
    x_test.to_csv('../processed_data/' + unit_key + '/train_test_splits/x_test.csv')
    y_train.to_csv('../processed_data/' + unit_key + '/train_test_splits/y_train.csv')
    y_test.to_csv('../processed_data/' + unit_key + '/train_test_splits/y_test.csv')
    player_names_train.to_csv('../processed_data/' + unit_key + '/train_test_splits/player_names_train.csv')
    player_names_test.to_csv('../processed_data/' + unit_key + '/train_test_splits/player_names_test.csv')


def read_train_test_split(unit_key):
    x_train = pd.read_csv('../processed_data/' + unit_key + '/train_test_splits/x_train.csv').iloc[:,
              1:]  # drop first column
    y_train = pd.read_csv('../processed_data/' + unit_key + '/train_test_splits/y_train.csv').iloc[:,
              1:]  # drop first column
    x_test = pd.read_csv('../processed_data/' + unit_key + '/train_test_splits/x_test.csv').iloc[:,
             1:]  # drop first column
    y_test = pd.read_csv('../processed_data/' + unit_key + '/train_test_splits/y_test.csv').iloc[:,
             1:]  # drop first column
    player_names_train = pd.read_csv(
        '../processed_data/' + unit_key + '/train_test_splits/player_names_train.csv').iloc[:, 1:]  # drop first column
    player_names_test = pd.read_csv('../processed_data/' + unit_key + '/train_test_splits/player_names_test.csv').iloc[
                        :, 1:]  # drop first column

    return x_train, x_test, y_train, y_test, player_names_train, player_names_test
