"""
This file loads data into Scikit-Learn bunches. It assumes the target data is in the last coumn of data. It will also apply the Scikit-Learn preprocessing scale function to standardize the dataset (http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.scale.html)

Code borrowed heavily from Benjamin Bengfort.
modified by Nicole Donnelly 20160513
"""
import os
import json
import numpy as np

from sklearn.datasets.base import Bunch
from sklearn import preprocessing

def load_data(data_file, root='data'):

    filenames     = {
        'meta': os.path.join(root, 'meta.json'),
        'data': os.path.join(root, data_file),
    }

    with open(filenames['meta'], 'r') as f:
        meta = json.load(f)
        target_names  = meta['target_names']
        feature_names = meta['feature_names']

    # Load the dataset from the text file.
    dataset = np.loadtxt(filenames['data'], delimiter=',')

    # Extract the target from the data
    target = dataset[:, -1]

    #extract and scale the data
    data   = dataset[:, 0:-1]
    data = preprocessing.scale(data)

    # Create the bunch object
    return Bunch(
        data=data,
        target=target,
        filenames=filenames,
        target_names=target_names,
        feature_names=feature_names,
    )
