# defense
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


# Average time in NFL for all positions: 3.3 years (no data found for defense)
#https://www.fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID=70&LeagueID=&order_by=Assist&sort_order=DESC
class DB:
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
    CLASSIFICATION_THRESHOLD = 0.5


# Average time in NFL for all positions: 3.3 years (no data found for defense)
#https://www.fftoday.com/stats/playerstats.php?Season=2021&GameWeek=&PosID=60&LeagueID=
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
    CLASSIFICATION_THRESHOLD = 0.5


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
        "Baseline",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
    ]

    classifiers = {
        'Baseline': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
    }

    params = {
        'Baseline': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'NearestNeighbors': {'n_neighbors': [2]},
        # Rbf c=0.01
        # Rbf c=0.001
        'SVC': {'kernel': ['rbf'],
                'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        'DecisionTree': {
            'max_depth': [5, 10, 40, 70, 100],  # 5, 10, 20, 40, 80, 150, 300, 500, 800, 1200],
            # Everything above 5 will basically already overfit the training data
            'min_samples_split': [0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8],
            'max_features': [1, 2, 3]
        },
        # max_depth=40, n_estimators=10, min_samples_split=0.2, min_samples_leaf=5, max_features=3, auc=0.73
        'RandomForest': {'max_depth': [5, 10, 15, 20, 25, 40, 80, 150, 300, 500, 800, 1200],
                         'n_estimators': [5, 10, 20, 30, 50, 80, 150, 300],
                         'min_samples_split': [0.2, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8],
                         'min_samples_leaf': [2, 3, 4, 5],
                         'max_features': [2, 3, 4, 5]
                         },
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
        "Baseline",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
    ]

    classifiers = {
        'Baseline': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
    }

    params = {
        'Baseline': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'NearestNeighbors': {'n_neighbors': [2]},
        # Rbf c=0.01
        # Rbf c=0.001
        'SVC': {'kernel': ['rbf'],
                'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        'DecisionTree': {
            'max_depth': [5, 10, 40, 70, 100],  # 5, 10, 20, 40, 80, 150, 300, 500, 800, 1200],
            # Everything above 5 will basically already overfit the training data
            'min_samples_split': [0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8],
            'max_features': [1, 2, 3]
        },
        # max_depth=40, n_estimators=10, min_samples_split=0.2, min_samples_leaf=5, max_features=3, auc=0.73
        'RandomForest': {'max_depth': [5, 10, 15, 20, 25, 40, 80, 150, 300, 500, 800, 1200],
                         'n_estimators': [5, 10, 20, 30, 50, 80, 150, 300],
                         'min_samples_split': [0.2, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8],
                         'min_samples_leaf': [2, 3, 4, 5],
                         'max_features': [2, 3, 4, 5]
                         },
    }


class RB:
    KEY = 'RB'
    MAX_YARD_THRESHOLD = 2.6 * 1000 * 2
    MAX_TD_THRESHOLD = 2.6 * 5 * 2
    MAX_REC_THRESHOLD = 2.6 * 20 * 2
    MAX_SEASON_THRESHOLD = 5.2
    CLASSIFICATION_THRESHOLD = 0.5

    # ml params
    names = [
        "Baseline",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
    ]

    classifiers = {
        'Baseline': DummyClassifier(),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
    }

    params = {
        'Baseline': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'NearestNeighbors': {'n_neighbors': [2]},
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
        'RandomForest': {'max_depth': [5, 15, 25],
                         'n_estimators': [5, 6, 20],
                         'min_samples_split': [3],
                         'min_samples_leaf': [3]
                         },
    }


class WR:
    KEY = 'WR'
    MAX_YARD_THRESHOLD = 2.8 * 1000 * 2
    MAX_TD_THRESHOLD = 2.8 * 5 * 2
    MAX_REC_THRESHOLD = 2.8 * 80 * 2
    MAX_SEASON_THRESHOLD = 5.6
    CLASSIFICATION_THRESHOLD = 0.5

    names = [
        "Baseline",
        "SVC",
        "NearestNeighbors",
        "DecisionTree",
        "RandomForest",
    ]

    classifiers = {
        'Baseline': DummyClassifier(),
        'SVC': SVC(random_state=4711),
        'NearestNeighbors': KNeighborsClassifier(),
        'DecisionTree': DecisionTreeClassifier(random_state=4711),
        'RandomForest': RandomForestClassifier(random_state=4711),
    }

    params = {
        'Baseline': {'strategy': ['most_frequent', 'stratified', 'uniform']},
        'NearestNeighbors': {'n_neighbors': [2, 3, 5]},
        # Rbf c=0.01
        # Rbf c=0.001
        'SVC': {'kernel': ['rbf'],
                'C': [0.01, 0.1, 1, 10, 1000],
                },
        # max_depth=150, min_samples_split=0.05, max_features=2,auc=0.71
        'DecisionTree': {
            'max_depth': [5, 10, 20],
            # Everything above 5 will basically already overfit the training data
            'min_samples_split': [0.05, 0.2, 0.4],
            'max_features': [2, 3, 4]
        },
        # max_depth=40, n_estimators=10, min_samples_split=0.2, min_samples_leaf=5, max_features=3, auc=0.73
        'RandomForest': {'max_depth': [5, 20],
                         'n_estimators': [5, 10, 20],
                         'min_samples_split': [0.05],
                         'min_samples_leaf': [2, 3],
                         'max_features': [2, 3]
                         },
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
