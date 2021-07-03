import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, accuracy_score

import utils.unit_keys as Units


def visualise_models(x_train, x_test, y_train, y_test, names_train, names_test, unit_key):
    print("Starting model evaluation for " + unit_key)
    grid_searches = joblib.load('../ml_models/' + unit_key + '_trained_models.sav')

    unit_class = Units.parse_unit(unit_key)

    results_test_acc = []
    results_test_std = []
    results_train_acc = []
    results_train_std = []
    labels = []

    for name in unit_class.names:
        test_acc = np.mean(grid_searches[name].cv_results_['mean_test_score'])
        results_test_acc.extend(grid_searches[name].cv_results_['mean_test_score'])
        results_test_std.extend(grid_searches[name].cv_results_['std_test_score'])
        results_train_acc.extend(grid_searches[name].cv_results_['mean_train_score'])
        results_train_std.extend(grid_searches[name].cv_results_['std_train_score'])
        for params in grid_searches[name].cv_results_['params']:
            label = name
            for param in params:
                label = label + '_' + param + ':' + str(params[param])
            labels.append(label)
            # print("Accuracy for " + label + ":" + str(test_acc))

    plt.barh(labels, results_test_acc)
    locs, ylabels = plt.yticks()
    plt.title(label='Test Accuracy Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_test_acc.png')
    plt.show()

    plt.barh(labels, results_train_acc)
    locs, ylabels = plt.yticks()
    plt.title(label='Training Accuracy Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_train_acc.png')
    plt.show()

    train_accuracies = []
    test_accuracies = []
    for name in unit_class.names:
        gs_test = grid_searches[name]

        # Concat label with params
        label = name + str(gs_test.best_params_)

        y_test_pred = gs_test.predict(x_test)

        df_comparison = pd.DataFrame()
        df_comparison['Name'] = names_test['full_player_name']
        df_comparison['Real'] = y_test['Classification_All']
        df_comparison['Prediction'] = y_test_pred
        df_comparison.to_csv('../ml_model_visualisations/' + unit_key + '/' + name + '_comparison.csv')

        print("Plotting some stats for model/params combination: " + label)
        # Confusion matrix
        # conf_matrix = confusion_matrix(y_test, y_test_pred)
        plot_confusion_matrix(estimator=gs_test, X=x_test, y_true=y_test)
        plt.title(label=label + 'confusion matrix')
        plt.savefig('../ml_model_visualisations/' + unit_key + '/' + name + '_conf_matrix.png')
        plt.show()

        # ROC curve for model
        metrics.plot_roc_curve(gs_test, x_test, y_test)
        plt.title(label=label + 'ROC AUC')
        plt.savefig('../ml_model_visualisations/' + unit_key + '/' + name + '_roc_curve.png')
        plt.show()

        test_acc = accuracy_score(y_test, y_test_pred)
        print("Accuracy for model: " + str(test_acc))
