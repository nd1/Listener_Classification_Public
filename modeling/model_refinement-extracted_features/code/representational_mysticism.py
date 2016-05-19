"""
Run the wrangled data through the models.
Begin by using the load_data function to create bunches.
Run across multiple datasets if they exist.

Nicole Donnelly 20160513
"""

import os
import load_data
import fit_and_evaluate

from sklearn.svm import SVC

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':

    #start_time = time.time()
    for root, dirs, files in os.walk('data'):
        for name in files:
            if name.endswith('.csv'):
                print (root + "/" + name)
                dataset = load_data.load_data(name, root)

                fit_and_evaluate.fit_and_evaluate(root, name, dataset, GaussianNB, "GaussianNB")

                fit_and_evaluate.fit_and_evaluate(root, name, dataset, LogisticRegression, "LogisticRegression")
