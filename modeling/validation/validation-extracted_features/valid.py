"""
Using the model with the highest recall value, run the validation sample (10K instances) and print out a classification_report showing the classifcation metrics.

Nicole Donnelly 20160516
"""

import load_data
import os
import pickle

from sklearn.metrics import classification_report

MODEL_DIR  = os.path.dirname(__file__)
MODEL = os.path.join(MODEL_DIR, "20kdistributed.txt.csv_gaussiannb.pickle")

with open(MODEL, 'rb') as gnb:
    gnb_model = pickle.load(gnb)

print "model loaded"

dataset = load_data.load_data('10k_validation.txt.csv')
print "datset loaded"
X = dataset.data
Y = dataset.target
print "ready to predict"
Y_ = gnb_model.predict(X)
print "predicted"
#print type(Y_)
print (classification_report(Y, Y_, target_names=["News", "Other"]))
