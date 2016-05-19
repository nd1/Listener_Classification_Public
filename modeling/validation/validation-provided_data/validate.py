"""
Using the model created with the provided data, run the provided validation data  and print out a classification_report showing the classifcation metrics.

Nicole Donnelly 20160516
"""

import os
import pickle
import numpy as np

from matplotlib.dates import strpdate2num
from sklearn import preprocessing
from sklearn.metrics import classification_report

MODEL_DIR  = os.path.dirname(__file__)
MODEL = os.path.join(MODEL_DIR, "gaussiannb.pickle")

with open(MODEL, 'rb') as gnb:
    gnb_model = pickle.load(gnb)

data_valid = np.loadtxt('datavalid.csv', delimiter=',', converters={5: strpdate2num('%H:%M:%S')})
print "datset loaded"

X = data_valid[:, 0:-1]
Y = data_valid[:, -1]

X = preprocessing.scale(X)
Y_ = gnb_model.predict(X)

print (classification_report(Y, Y_, target_names=["News", "Other"]))
