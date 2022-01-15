import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, accuracy_score, roc_auc_score

import utils.unit_keys as Units


def encode_array_numeric(array):
    result_array = []
    for element in array:
        if element == 'Bust':
            result_array.append(0)
        else:
            result_array.append(1)
    return result_array

# Visualize model performance according to different metrics:
# - ROC: Receiver operating characteristic (TPR vs FPR): This curve is visualized for the best models in each category
# - AUC: Area-under-curve is calculated to compare models with each other
# - Accuracy
# - Confusion matrices
def visualise_models(x_train, x_test, y_train, y_test, names_train, names_test, unit_key):
    print("Starting model evaluation for " + unit_key)
    grid_searches = joblib.load('../ml_models/' + unit_key + '_trained_models.sav')

    unit_class = Units.parse_unit(unit_key)
    scoring = grid_searches['Baseline'].scoring
    labels = []
    train_accuracies = []
    test_accuracies = []
    test_rocauc_scores = []
    train_rocauc_scores = []

    y_test_predictions = []

    for name in unit_class.names:
        gs_test = grid_searches[name]

        # Concat label with params
        label = name + str(gs_test.best_params_)

        y_test_pred = gs_test.predict(x_test)
        y_train_pred = gs_test.predict(x_train)

        df_comparison = pd.DataFrame()
        df_comparison['Name'] = names_test['full_player_name']
        df_comparison['Real'] = y_test['Classification_All']
        df_comparison['Prediction'] = y_test_pred
        df_comparison.to_csv('../ml_model_visualisations/' + unit_key + '/' + name + '_comparison.csv')

        print("Plotting some stats for model/params combination: " + label)
        # Confusion matrix
        plot_confusion_matrix(estimator=gs_test, X=x_test, y_true=y_test)
        plt.title(label=label + 'confusion matrix')
        plt.savefig('../ml_model_visualisations/' + unit_key + '/' + name + '_conf_matrix.png')
        plt.show()

        # ROC curve for model
        metrics.plot_roc_curve(gs_test, x_test, y_test)
        plt.title(label=label + 'ROC AUC')
        plt.savefig('../ml_model_visualisations/' + unit_key + '/' + name + '_roc_curve.png')
        plt.show()

        y_test_num = encode_array_numeric(y_test['Classification_All'].values)
        y_test_pred_num = encode_array_numeric(y_test_pred)
        y_train_num = encode_array_numeric(y_train['Classification_All'].values)
        y_train_pred_num = encode_array_numeric(y_train_pred)

        test_rocauc = roc_auc_score(y_test_num, y_test_pred_num)
        train_rocauc = roc_auc_score(y_train_num, y_train_pred_num)
        test_rocauc_scores.append(test_rocauc)
        train_rocauc_scores.append(train_rocauc)

        test_acc = accuracy_score(y_test, y_test_pred)
        train_acc = accuracy_score(y_train, y_train_pred)
        test_accuracies.append(test_acc)
        train_accuracies.append(train_acc)
        labels.append(label)

        y_test_predictions.append(y_test_pred_num)

    # Collected ROC curve for models
    plt.figure()

    for i in range(0, len(y_test_predictions)):
        name = unit_class.names[i]
        gs = grid_searches[name]

        y_score = y_test_predictions[i]
        fpr, tpr, _ = metrics.roc_curve(y_test, y_score, pos_label='Good')
        plt.plot(fpr, tpr, label=name + " (AUC= {0:0.2f}".format(test_rocauc_scores[i]) + ")")

    plt.legend(loc=4)
    plt.title(label='ROC AUC Curve')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.savefig('../ml_model_visualisations/' + unit_key + '/' + 'combined_roc_curve.png')
    plt.show()

    # RocAuc plots
    plt.barh(labels, test_rocauc_scores)
    locs, ylabels = plt.yticks()
    plt.title(label='Test AUC Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_test_auc.png')
    plt.show()

    plt.barh(labels, train_rocauc_scores)
    locs, ylabels = plt.yticks()
    plt.title(label='Training AUC Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_train_auc.png')
    plt.show()

    # Accuracy plots
    plt.barh(labels, test_accuracies)
    locs, ylabels = plt.yticks()
    plt.title(label='Test Accuracy Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_test_acc.png')
    plt.show()

    plt.barh(labels, train_accuracies)
    locs, ylabels = plt.yticks()
    plt.title(label='Training Accuracy Comparison')
    plt.yticks(ticks=locs, labels=labels, fontsize=9)
    plt.tight_layout()
    plt.savefig('../ml_model_visualisations/' + unit_key + '/model_comparison_train_acc.png')
    plt.show()
