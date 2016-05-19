"""
Rank features of scaled data using ExtraTreesClassifier

Nicole Donnelly 20160512
"""

import os
import numpy as np
import load_data

from sklearn import cross_validation as cv
from sklearn.cross_validation import train_test_split as tts
from sklearn.ensemble import ExtraTreesClassifier

for root, dirs, files in os.walk('data'):
    for name in files:
        if name.endswith('.csv'):
            print "Loading " + root + "/" + name
            dataset = load_data.load_data(name, root)

            splits = tts(dataset.data, dataset.target, test_size=0.2)
            X_train, X_test, y_train, y_test = splits

            # Build a forest and compute the feature importances
            forest = ExtraTreesClassifier(n_estimators=250)
            forest.fit(X_train, y_train)
            importances = forest.feature_importances_
            std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
            indices = np.argsort(importances)[::-1]

             # Print the feature ranking
            print("Feature ranking:")

            for f in range(X_train.shape[1]):
                print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
