# defense
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn.tree import DecisionTreeClassifier


# Average time in NFL for all positions: 3.3 years (no data found for defense)
# https://www.fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID=70&LeagueID=&order_by=Assist&sort_order=DESC
class DB:  #
    KEY = 'DB'
    MAX_CAUGHT_INTS_THRESHOLD = 3.3 * 2 * 2
    MAX_INCOMPLETE_PASSES_THRESHOLD = 3.3 * 2 * 7.5
    MAX_TOT_TACKLES_THRESHOLD = 3.3 * 2 * 30
    MAX_ASS_TACKLES_THRESHOLD = 3.3 * 2 * 20
    MAX_SOLO_TACKLE_THRESHOLD = 3.3 * 2 * 10
    MAX_TFL_THRESHOLD = 3.3 * 2 * 1
    MAX_SACK_THRESHOLD = 3.3 * 2 * 1
    MAX_FORCED_FUMBLES_THRESHOLD = 3.3 * 2 * 1
    MAX_SEASON_THRESHOLD = 5.6  # (taken from WR)
    CLASSIFICATION_THRESHOLD = 0.4

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [11]},
        # Accuracy for best SVC{'kernel': 'poly', 'degree': 4, 'C': 0.0001} model
        # Accuracy for best SVC{'C': 100000, 'kernel': 'rbf'} model --> 0.09, 0.63
        # 10000, rbf --> 0.69, 0.10
        # 1000, rbf --> 0.74, 0.15
        # 100, rbf --> 0.78, 0.22
        # 10 already goes towards less accuracy
        'SVC': {'kernel': ['rbf'],  # 'logistic', 'poly'
                'C': [100],
                },
        # Accuracy for best DecisionTree{'max_depth': 10, 'max_features': 4, 'min_samples_leaf': 1, 'min_samples_split': 0.05} model
        # 0.68, 0.15
        'DecisionTree': {
            'max_depth': [20],
            'min_samples_split': [0.075],
            'min_samples_leaf': [1],
            'max_features': [6]
        },
        # Accuracy for best RandomForest{'max_depth': 20, 'max_features': 3, 'min_samples_leaf': 2, 'min_samples_split': 0.05, 'n_estimators': 64} model
        # 0.78, 0.16
        'RandomForest': {'max_depth': [15],
                         'n_estimators': [70],
                         'min_samples_split': [0.9],
                         'min_samples_leaf': [1],
                         'max_features': [3]
                         },

        # Accuracy for best NN{'max_iter': 500, 'learning_rate': 'adaptive', 'hidden_layer_sizes': 250, 'early_stopping': False, 'batch_size': 150, 'alpha': 0.01, 'activation': 'tanh'}
        # Accuracy for best NN{'max_iter': 1000, 'learning_rate': 'constant', 'hidden_layer_sizes': 1000, 'early_stopping': False, 'batch_size': 100, 'alpha': 0.001, 'activation': 'tanh'}
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.001, 'batch_size': 100, 'early_stopping': False, 'hidden_layer_sizes': 1000, 'learning_rate': 'constant', 'max_iter': 1000}, 0.7, 0.15
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.001, 'batch_size': 100, 'early_stopping': False, 'hidden_layer_sizes': 1000, 'learning_rate': 'constant', 'max_iter': 1000} 0.7, 0.15
        'NN': {'hidden_layer_sizes': [1000],
               'alpha': [0.01],  # try with one bigger, to maybe prevent overfitting
               'activation': ['tanh'],
               'batch_size': [100],
               'learning_rate': ['constant'],
               'max_iter': [500],
               'early_stopping': [True]
               }
    }


# Average time in NFL for all positions: 3.3 years (no data found for defense)
# https://www.fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID=60&LeagueID=
class LB:
    KEY = 'LB'
    MAX_SACK_THRESHOLD = 3.3 * 3 * 2
    MAX_TOT_TACKLES_THRESHOLD = 3.3 * 75 * 2
    MAX_ASS_TACKLES_THRESHOLD = 3.3 * 27.5 * 2
    MAX_SOLO_TACKLE_THRESHOLD = 3.3 * 40 * 2
    MAX_TFL_THRESHOLD = 3.3 * 5 * 2
    MAX_QB_HITS_THRESHOLD = 3.3 * 6 * 2
    MAX_FORCED_FUMBLES_THRESHOLD = 3.3 * 1.5 * 2
    MAX_INCOMPLETE_PASSES_THRESHOLD = 3.3 * 5 * 2
    MAX_CAUGHT_INTS_THRESHOLD = 3.3 * 0.5 * 2
    MAX_SEASON_THRESHOLD = 5.2  # (taken from RB)
    CLASSIFICATION_THRESHOLD = 0.45

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "NearestNeighbors",
        "SVC",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [13, 14, 15]},
        # Accuracy for best SVC{'C': 10000, 'kernel': 'rbf'} model, 0.44, 0.18
        # Accuracy for best SVC{'C': 1000, 'degree': 4, 'kernel': 'poly'}, 0.67, 0.17
        # Accuracy for best SVC{'C': 10000, 'degree': 3, 'kernel': 'poly'} 0.71, 0.18
        'SVC': {'kernel': ['poly'],  # logistic, poly
                'C': [10000],  # 0.00001, 0.0001, 100000
                'degree': [3],
                },
        # 0.65, 0.10 - {'max_depth': 20, 'max_features': 3, 'min_samples_leaf': 1, 'min_samples_split': 0.05}
        # 0.59, 0.07 - {'max_depth': 17, 'max_features': 6, 'min_samples_leaf': 2, 'min_samples_split': 0.05}
        # worse {'max_depth': 20, 'max_features': 5, 'min_samples_leaf': 1, 'min_samples_split': 0.05} model
        'DecisionTree': {
            'max_depth': [20],
            'min_samples_split': [0.05],
            'min_samples_leaf': [1],
            'max_features': [3]
        },
        # 0.79, 0.13 - {'max_depth': 20, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.05, 'n_estimators': 64}
        # 0.78, 0.12 - {'max_depth': 19, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.05, 'n_estimators': 60}
        #  same - {'max_depth': 20, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.05, 'n_estimators': 62} model
        # 0.80, 0.13 - {'max_depth': 20, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.06, 'n_estimators': 64}
        'RandomForest': {'max_depth': [20],
                         'n_estimators': [64],
                         'min_samples_split': [0.075],
                         'min_samples_leaf': [2],
                         'max_features': [4]
                         },
        # 0.64, 0.06, overfitting, {'max_iter': 1000, 'learning_rate': 'adaptive', 'hidden_layer_sizes': 500, 'early_stopping': False, 'batch_size': 600, 'alpha': 0.001, 'activation': 'tanh'}
        #0.62, 0.06, overfitting {'max_iter': 1000, 'learning_rate': 'constant', 'hidden_layer_sizes': 250, 'early_stopping': False, 'batch_size': 600, 'alpha': 0.1, 'activation': 'tanh'}
        # 0.64, 0.04 {'activation': 'tanh', 'alpha': 0.01, 'batch_size': 600, 'early_stopping': False, 'hidden_layer_sizes': 250, 'learning_rate': 'constant', 'max_iter': 1000} model
        # best: 0.8, 0.17
        'NN': {'hidden_layer_sizes': [750],
               'alpha': [0.001],
               'activation': ['tanh'],
               'batch_size': [600],
               'learning_rate': ['constant'],
               'max_iter': [1000],
               'early_stopping': [True]
               },
    }
    # Average time in NFL for all positions: 3.3 years (no data found for defense)
    # https://www.pro-football-reference.com/years/2020/defense.htm
    # NOTE: Classification will e.g. label N.Bosa as Bust because it takes total amounts


class DL:
    KEY = 'DL'
    MAX_SACK_THRESHOLD = 3.3 * 5 * 2
    MAX_QB_HITS_THRESHOLD = 3.3 * 10 * 2
    MAX_TFL_THRESHOLD = 3.3 * 5 * 2
    MAX_TOT_TACKLES_THRESHOLD = 3.3 * 15 * 2
    MAX_ASS_TACKLES_THRESHOLD = 3.3 * 5 * 2
    MAX_SOLO_TACKLE_THRESHOLD = 3.3 * 10 * 2
    MAX_FORCED_FUMBLES_THRESHOLD = 3.3 * 1 * 2
    MAX_SEASON_THRESHOLD = 5.2  # (taken from RB)
    CLASSIFICATION_THRESHOLD = 0.35

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
        'SVC': {'kernel': ['rbf'],
                'C': [10000],  # 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        # {'max_depth': 20, 'max_features': 2, 'min_samples_leaf': 1, 'min_samples_split': 0.05} model
        # {'max_depth': 21, 'max_features': 2, 'min_samples_leaf': 1, 'min_samples_split': 0.03} model
        # {'max_depth': 21, 'max_features': 2, 'min_samples_leaf': 1, 'min_samples_split': 0.01} model
        'DecisionTree': {
            'max_depth': [21],
            'min_samples_split': [0.04],
            'min_samples_leaf': [1],
            'max_features': [2]
        },
        # Accuracy for best RandomForest{'max_depth': 20, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.05, 'n_estimators': 32} model
        # Accuracy for best RandomForest{'max_depth': 22, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.03, 'n_estimators': 36} model
        # Accuracy for best RandomForest{'max_depth': 22, 'max_features': 4, 'min_samples_leaf': 2, 'min_samples_split': 0.01, 'n_estimators': 38} model
        'RandomForest': {'max_depth': [22],
                         'n_estimators': [38],
                         'min_samples_split': [0.05],
                         'min_samples_leaf': [2],
                         'max_features': [4]
                         },
        # NN{'max_iter': 1500, 'learning_rate': 'invscaling', 'hidden_layer_sizes': 500, 'early_stopping': False, 'batch_size': 50, 'alpha': 0.001, 'activation': 'tanh'} model, 0.62, 0.10
        # NN{'max_iter': 2000, 'learning_rate': 'constant', 'hidden_layer_sizes': 100, 'early_stopping': False, 'batch_size': 150, 'alpha': 0.001, 'activation': 'tanh'} model, 0.67, 0.12
        # NN{'max_iter': 1500, 'learning_rate': 'constant', 'hidden_layer_sizes': 250, 'early_stopping': False, 'batch_size': 50, 'alpha': 0.001, 'activation': 'tanh'} model
        # NN{'activation': 'tanh', 'alpha': 0.001, 'batch_size': 50, 'early_stopping': False, 'hidden_layer_sizes': 500, 'learning_rate': 'constant', 'max_iter': 1000}
        # NN{'activation': 'tanh', 'alpha': 0.0001, 'batch_size': 150, 'early_stopping': False, 'hidden_layer_sizes': 100, 'learning_rate': 'constant', 'max_iter': 1900}, 0,72, 0,15
        # NN{'activation': 'tanh', 'alpha': 0.0001, 'batch_size': 150, 'early_stopping': False, 'hidden_layer_sizes': 100, 'learning_rate': 'constant', 'max_iter': 1850}
        'NN': {'hidden_layer_sizes': [100],
               'alpha': [0.0001],
               'activation': ['tanh'],
               'batch_size': [150],
               'learning_rate': ['constant'],
               'max_iter': [860],
               'early_stopping': [True]
               }
    }


# unused
OL = 'OL'
K = 'K'


# Average time in NFL for offense positions:
# https://www.statista.com/statistics/240102/average-player-career-length-in-the-national-football-league/
# offense
class TE:
    KEY = 'TE'
    # using WR time in NFL as TE no data was found
    MAX_YARD_THRESHOLD = 2.8 * 800 * 2
    MAX_TD_THRESHOLD = 2.8 * 3 * 2
    MAX_REC_THRESHOLD = 2.8 * 50 * 2
    MAX_SEASON_THRESHOLD = 5.6
    CLASSIFICATION_THRESHOLD = 0.5

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [5]},
        'SVC': {'kernel': ['rbf'],
                'C': [100000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        'DecisionTree': {
            'max_depth': [16],
            'min_samples_split': [0.02],
            'min_samples_leaf': [1],
            'max_features': [1]
        },
        'RandomForest': {'max_depth': [8],
                         'n_estimators': [55],
                         'min_samples_split': [0.05],
                         'min_samples_leaf': [2],
                         'max_features': [1]
                         },
        # 'max_iter': 1000, 'learning_rate': 'constant', 'hidden_layer_sizes': 100, 'early_stopping': False, 'batch_size': 10, 'alpha': 0.001, 'activation': 'relu'
        'NN': {'hidden_layer_sizes': [100],
               'alpha': [0.001],
               'activation': ['relu'],
               'batch_size': [10],
               'learning_rate': ['constant'],
               'max_iter': [900],
               'early_stopping': [False]
               }
    }


class QB:
    KEY = 'QB'
    MAX_YARD_THRESHOLD = 4.4 * 2250 * 2
    MAX_TD_THRESHOLD = 4.4 * 10 * 2
    MAX_INT_THRESHOLD = 4.4 * 5 * 2  # not suitable
    # go with 300 per regular season
    # https://www.pro-football-reference.com/years/NFL/passing.htm
    MAX_COMP_THRESHOLD = 4.4 * 300 * 2
    MAX_SEASON_THRESHOLD = 8.8
    CLASSIFICATION_THRESHOLD = 0.4

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [2]},
        # Rbf c=0.01
        # Rbf c=0.001
        'SVC': {'kernel': ['rbf'],  # , 'sigmoid', 'linear'],
                'C': [1000, 10000, 100000],  # 0.001, 0.01, 0.1, 1, 10, 100,
                },
        # max_depth=15, min_samples_split=0.05, max_features=2
        'DecisionTree': {
            'max_depth': [15],  # 5, 10, 20, 40, 80, 150, 300, 500, 800, 1200],
            # Everything above 5 will basically already overfit the training data
            'min_samples_split': [0.05],
            'max_features': [2]
        },
        # max_depth=40, n_estimators=10, min_samples_split=0.2, min_samples_leaf=5, max_features=3, auc=0.73
        'RandomForest': {'max_depth': [15],
                         'n_estimators': [35],
                         'min_samples_split': [0.02],
                         'min_samples_leaf': [1],
                         'max_features': [3]
                         },
        # alpha: 0.001, batch_size: 475, activation: logistic, hidden_layers: 195, learning rate: constant, max_iter: 1300, early_stopping: False
        'NN': {'hidden_layer_sizes': [195],
               'alpha': [0.001],
               'activation': ['logistic'],
               'batch_size': [475],
               'learning_rate': ['constant'],
               'max_iter': [1300],
               'early_stopping': [False]
               }
    }


class RB:
    KEY = 'RB'
    MAX_YARD_THRESHOLD = 2.6 * 1000 * 2
    MAX_TD_THRESHOLD = 2.6 * 5 * 2
    MAX_REC_THRESHOLD = 2.6 * 20 * 2
    MAX_SEASON_THRESHOLD = 5.2
    CLASSIFICATION_THRESHOLD = 0.3

    # ml params
    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'NearestNeighbors': KNeighborsClassifier(),
        'SVC': SVC(random_state=4711),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711, n_jobs=-1),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [2]},
        'SVC': {'kernel': ['rbf'],  # , 'sigmoid', 'linear', poly ],
                'C': [10000, 100000],  # 0.001, 0.01, 0.1, 1, 10, 100,
                # 'degree': [2, 3, 4]
                },
        # Decision Tree best random search:
        # min_samples_split=0.9, max_features=3, max_depth=10 (roc_auc=0.59)
        # min_samples_split=0.1, max_features=3, max_depth=40 (roc_auc=0.58)
        'DecisionTree': {
            'max_depth': [5],
            # Everything above 5 will basically already overfit the training data
            'min_samples_split': [0.2],
            'max_features': [2],
            'min_samples_leaf': [1]
        },
        'RandomForest': {'max_depth': [5],
                         'n_estimators': [40],
                         'min_samples_split': [5],
                         'min_samples_leaf': [2]
                         },
        'NN': {'hidden_layer_sizes': [230],
               'alpha': [10000],
               'activation': ['logistic'],
               'batch_size': [220],
               'learning_rate': ['invscaling'],
               'max_iter': [775],
               'early_stopping': [False]
               }
    }


class WR:
    KEY = 'WR'
    MAX_YARD_THRESHOLD = 2.8 * 1000 * 2
    MAX_TD_THRESHOLD = 2.8 * 5 * 2
    MAX_REC_THRESHOLD = 2.8 * 80 * 2
    MAX_SEASON_THRESHOLD = 5.6
    CLASSIFICATION_THRESHOLD = 0.35

    names = [
        "Baseline_best",
        "Baseline_MostFrequent",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
        "NN",
    ]

    classifiers = {
        'Baseline_best': DummyClassifier(),
        'Baseline_MostFrequent': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711, n_jobs=-1),
        'NN': MLPClassifier(random_state=4711)
    }

    params = {
        'Baseline_best': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'Baseline_MostFrequent': {'strategy': ['most_frequent']},
        'NearestNeighbors': {'n_neighbors': [5]},
        'SVC': {'kernel': ['rbf'],
                'C': [100000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        'DecisionTree': {
            'max_depth': [17],
            'min_samples_split': [0.08],
            'min_samples_leaf': [1],
            'max_features': [3]
        },
        # max_depth=40, n_estimators=10, min_samples_split=0.2, min_samples_leaf=5, max_features=3, auc=0.73
        'RandomForest': {'max_depth': [18],
                         'n_estimators': [80],
                         'min_samples_split': [0.05],
                         'min_samples_leaf': [1],
                         'max_features': [2]
                         },
        # Accuracy for best NN{'max_iter': 500, 'learning_rate': 'invscaling', 'hidden_layer_sizes': 1000, 'early_stopping': False, 'batch_size': 50, 'alpha': 0.001, 'activation': 'tanh'} model
        # Accuracy for best NN{'max_iter': 1500, 'learning_rate': 'invscaling', 'hidden_layer_sizes': 500, 'early_stopping': False, 'batch_size': 600, 'alpha': 1, 'activation': 'tanh'} model
        # Accuracy for best NN{'max_iter': 2000, 'learning_rate': 'constant', 'hidden_layer_sizes': 1000, 'early_stopping': False, 'batch_size': 600, 'alpha': 1, 'activation': 'tanh'} model
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.01, 'batch_size': 500, 'early_stopping': False, 'hidden_layer_sizes': 1000, 'learning_rate': 'constant', 'max_iter': 1000} model
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.005, 'batch_size': 500, 'early_stopping': False, 'hidden_layer_sizes': 1000, 'learning_rate': 'constant', 'max_iter': 1250} model
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.001, 'batch_size': 480, 'early_stopping': False, 'hidden_layer_sizes': 1000, 'learning_rate': 'constant', 'max_iter': 1000} model
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.01, 'batch_size': 490, 'early_stopping': False, 'hidden_layer_sizes': 950, 'learning_rate': 'constant', 'max_iter': 950} model
        # Accuracy for best NN{'activation': 'tanh', 'alpha': 0.003, 'batch_size': 495, 'early_stopping': False, 'hidden_layer_sizes': 975, 'learning_rate': 'constant', 'max_iter': 925} model

        'NN': {'hidden_layer_sizes': [975],
               'alpha': [0.003],  # 0.001, 0.005,
               'activation': ['tanh'],
               'batch_size': [495],
               'learning_rate': ['constant'],
               'max_iter': [925],
               'early_stopping': [False]
               }
    }


def parse_unit(unit_key):
    if unit_key == RB.KEY:
        return RB
    if unit_key == WR.KEY:
        return WR
    if unit_key == TE.KEY:
        return TE
    if unit_key == QB.KEY:
        return QB
    if unit_key == DB.KEY:
        return DB
    if unit_key == LB.KEY:
        return LB
    if unit_key == DL.KEY:
        return DL
    return None


def get_unit_list():
    return [WR.KEY, RB.KEY, QB.KEY, TE.KEY, DB, LB, DL]
