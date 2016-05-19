"""
Use scikit-learn to fit/ evaluate models.

Code borrowed heavily from Benjamin Bengfort.
modified by Nicole Donnelly 20160513
"""

import os
import time
import pickle

import pandas as pd

from sklearn import preprocessing
from sklearn import metrics
from sklearn import cross_validation
from sklearn.cross_validation import KFold

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression


def fit_and_evaluate(data_train, data_test, model, label, **kwargs):
    """
    Because of the Scikit-Learn API, we can create a function to
    do all of the fit and evaluate work on our behalf!
    """
    start  = time.time()

    #create empty lists for scoring variables
    scores = {'precision':[], 'recall':[], 'accuracy':[], 'f1':[]}

    #split then scale the data. fit the model and make predictions
    for train, test in KFold(data_train.shape[0], n_folds=12, shuffle=True):
        X_train, X_test = data_train[:, 0:-1], data_test[:, 0:-1]
        y_train, y_test = data_train[:, -1], data_test[:, -1]

        X_train = preprocessing.scale(X_train)
        X_test = preprocessing.scale(X_test)

        estimator = model(**kwargs)
        estimator.fit(X_train, y_train)
        expected  = y_test
        predicted = estimator.predict(X_test)

        scores = {'precision':[], 'recall':[], 'accuracy':[], 'f1':[]}
        scores['precision'].append(metrics.precision_score(expected, predicted, average='binary'))
        scores['recall'].append(metrics.recall_score(expected, predicted, average='binary'))
        scores['accuracy'].append(metrics.accuracy_score(expected, predicted))
        scores['f1'].append(metrics.f1_score(expected, predicted, average='binary'))

    # Report
    print "Build and Validation of {} took {:0.3f} seconds".format(label, time.time()-start)
    print "Validation scores are as follows:\n"
    print pd.DataFrame(scores).mean()

    #print feature weights. these have been computed separately for tree models.
    if label == "LogisticRegression":
        print estimator.coef_
    if label == "GaussianNB":
        print estimator.class_prior_

    # Write official estimator to disk
    estimator = model(**kwargs)
    estimator.fit(X_train, y_train)

    outpath = label.lower().replace(" ", "-") + ".pickle"
    with open(outpath, 'w') as f:
        pickle.dump(estimator, f)

    print "\nFitted model written to:\n{}".format(os.path.abspath(outpath))
