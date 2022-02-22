import joblib
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import python_scripts.football_utility_functions as nfl
import utils.unit_keys as Units


# 1. Read in WR data
# 2. Remove any data that we don't have at that point in time
# 3. Split into train/test
# 4. Split into X/Y
# 5. Train a model
# 6. Evaluate model

def add_array_to_df_as_rows(array, df):
    return df.append(pd.DataFrame(array, columns=list(df)))


def start_ml_pipeline(unit_key=Units.WR.KEY, scoring='roc_auc', random_search=False, unbalanced=False):
    print("Started ML pipeline for " + unit_key.upper())
    ml_dataset = nfl.read_merged_file_for_unit(unit_key)

    unit_class = Units.parse_unit(unit_key)

    # do for all units
    # ml_dataset['age'] = ml_dataset['age'].fillna(value=ml_dataset.mean()['age'])
    # drop gsis_id since this will often be NaN for players that didn't make the roster
    ml_dataset.drop(inplace=True, columns='gsis_id')
    ml_dataset.dropna(inplace=True)

    # feature selection for specific unit key
    x = nfl.select_features_for_unit(ml_dataset, unit_key)
    y = ml_dataset[['Classification_All']]

    vis = pd.DataFrame(x)
    vis = vis.drop(columns='full_player_name')
    vis['Classification_All'] = y[['Classification_All']]

    # check the features we selected in scatterplot
    scatter_plot = sns.pairplot(vis, hue='Classification_All', diag_kind='scatter')
    scatter_plot.savefig('../ml_models/feature_selection/' + unit_key + '_featureplot.png')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42069)

    player_names_train = x_train['full_player_name']
    player_names_test = x_test['full_player_name']
    x_train.drop(columns='full_player_name', inplace=True)
    x_test.drop(columns='full_player_name', inplace=True)

    print("Classification counts for the data:")
    print("Training data: " + str(y_train.value_counts()))
    print("Test data: " + str(y_test.value_counts()))

    # resample unbalanced classes for better training
    if unbalanced:
        train_shape = y_train['Classification_All'].value_counts()
        if train_shape[0] >= train_shape[1]:
            sample_amount = train_shape[0] - train_shape[1]
        else:
            sample_amount = train_shape[1] - train_shape[0]
        x_balance_samples, y_balance_samples = resample(x_train[y_train['Classification_All'] == 'Good'].to_numpy(),
                                                        y_train[y_train['Classification_All'] == 'Good'].to_numpy(),
                                                        replace=True,
                                                        n_samples=sample_amount,
                                                        random_state=4711)
        x_train = add_array_to_df_as_rows(x_balance_samples, x_train)
        y_train = add_array_to_df_as_rows(y_balance_samples, y_train)

        print("AFTER RESAMPLING: Classification counts for the data:")
        print("Training data: " + str(y_train.value_counts()))
        print("Test data: " + str(y_test.value_counts()))

    kfold = KFold(n_splits=3, shuffle=True, random_state=4711)
    grid_searches = {}

    # fit for all defined models and parameter configurations
    for name in unit_class.names:
        model = unit_class.classifiers[name]
        parameterset = unit_class.params[name]

        if random_search:
            print("Running RandomizedSearchCV for %s." % name)
            gs = RandomizedSearchCV(model, parameterset, cv=kfold, n_iter=100, scoring=scoring, verbose=0,
                                    return_train_score=True)
        else:
            print("Running GridSearchCV for %s." % name)
            gs = GridSearchCV(model, parameterset, cv=kfold, scoring=scoring, verbose=0, return_train_score=True)

        gs.fit(x_train, y_train.iloc[:, 0])
        grid_searches[name] = gs

    joblib.dump(grid_searches, '../ml_models/' + unit_key + '_trained_models.sav')
    return x_train, x_test, y_train, y_test, player_names_train, player_names_test
