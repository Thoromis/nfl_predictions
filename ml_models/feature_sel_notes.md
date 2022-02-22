# Feature selection notes

## QBs

In the scatter plot for QBs you can see a couple of things about the features, upon which I decided to leave out some
features.

- Rush Attempts, Rush Yards and Rush TDs all provide very valuable information, which, between the three, is only a
  correlating slightly, but not too much. Will include all three!
- I'll drop Pass Yards, as it holds too much similar information with both Pass TDs and Pass Completions.
- Pass Ints will be included, as it holds good new information compared e.g. with Pass TDs.
- Pass Attempts is conflicting, doesn't hold too much information that Pass Completions does not yet hold, but it is
  able to differentiate in a couple of edge cases (very high attempt ratio).
- Comp Percentage will be included as it doesn't really correlate with any of the existing features so far.

![here](./feature_selection/QB_featureplot.png)

## Best models

- Random Forest: max_depth: 15, max_features: 3, min_samples_leaf: 1, min_samples_split: 0.02, n_estimators: 35
- Nearest Neighbors: 2
- MLP: alpha: 0.001, batch_size: 475, activation: logistic, hidden_layers: 195, learning rate: constant, max_iter: 1300,
  early_stopping: False
- Decision Trees: max_depth=15, min_samples_split=0.05, max_features=2
- SVC: C: 10000, kernel: rbf

## RBs

For RBs, depending again on the scatter plot, the following features can be sorted out/used:

- Rush Att and Rush Yards hold the same information - Yards will be chosen
- Receptions and Reception Yards hold the same information - Yards will be chosen
- The other features should hold a fair amount of information about the classification problem.

![here](./feature_selection/RB_featureplot.png)

## Best Models

- Nearest Neighbors: n_neighbors=2 (or 5)
- SVC: kernel=rbf, C=100000
- MLP: NN{'activation': 'logistic', 'alpha': 10000, 'batch_size': 220, 'early_stopping': False, 'hidden_layer_sizes': 230, 'learning_rate': 'invscaling', 'max_iter': 775}
- Decision Trees: {'max_depth': 5, 'max_features': 2, 'min_samples_leaf': 1, 'min_samples_split': 0.2}
- Random Forest: {'max_depth': 5, 'min_samples_leaf': 2, 'min_samples_split': 5, 'n_estimators': 40}

## NOTES

### Precision and Recall

If our model predicted 30 Good players, but only 3 of them are really Good, our precision is 3/30. If our model
predicted 30 Good players, 3 of them correctly, and there are 20 overall Good players, our recall is 3/20.

Ideally, we wanna be good in both values, but we are very bad in precision.

### Neural Network starting params:
alpha parameter is used as overfitting measure by adding weight decay, penalizing large weights in the network. 


```'NN': {'hidden_layer_sizes': [10, 100, 250, 500, 1000],
               'alpha': [0.001, 0.01, 0.1, 1],
               'activation': ['logistic', 'tanh', 'relu', 'identity'],
               'batch_size': [10, 50, 100, 150, 200, 400, 600],
               'learning_rate': ['constant', 'invscaling', 'adaptive'],
               'max_iter': [500, 1000, 1500, 2000],
               'early_stopping': [False, True]
               }```
