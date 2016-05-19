"""
Run the wrangled data through the models.

Nicole Donnelly 20160513
"""

import os
#import load_data
import fit_and_evaluate

import numpy as np
from matplotlib.dates import strpdate2num

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':

    #load the data
    data_train = np.loadtxt('datatrain.csv', delimiter=',', converters={5: strpdate2num('%H:%M:%S')})
    data_test = np.loadtxt('datatest.csv', delimiter=',', converters={5: strpdate2num('%H:%M:%S')})

    fit_and_evaluate.fit_and_evaluate(data_train, data_test, GaussianNB, "GaussianNB")
    fit_and_evaluate.fit_and_evaluate(data_train, data_test, LogisticRegression, "LogisticRegression")
