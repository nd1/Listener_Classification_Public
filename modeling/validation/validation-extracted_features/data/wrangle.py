#!/usr/bin/env python
"""
This file modifies the data set and creates the meta.json and pandas dataset.csv files from theinitial data.

This file should be run in the data directory and will look for txt files in subdirectories to process if multiple datasets are available.

Code originally created by Benjamin Bengfort.
modified by Nicole Donnelly 20160506
"""

import os
import glob
import json
import pandas as pd


FEATURES  = ['prev_duration', 'prev_avg_rating_news', 'prev_avg_rating_podcast', 'prev_shift', 'time_diff_hr']

LABEL_MAP = {
    0: 'Not Podcast',
    1: 'Podcast'
}

DROP_FEATURES = ['row', 'user', 'prev_session_id', 'next_session_id',
       'next_duration', 'prev_num_ratings', 'next_num_ratings',
       'next_avg_rating_news', 'next_avg_rating_podcast',
       'next_shift', 'prev_num_news', 'prev_num_podcast', 'next_num_news',
       'next_num_podcast', 'prev_platform', 'next_platform',
       'prev_num_complete', 'prev_num_thumbup', 'prev_num_skip',
       'prev_num_searchcomplete', 'next_num_complete', 'next_num_thumbup',
       'next_num_skip', 'next_num_searchcomplete']

if __name__ == "__main__":

#create a headerless csv file for each txt file dropping the specified columns
#create a json file in each data subdirectory

    for root, dirs, files in os.walk('data', topdown=False):
        for name in files:
            if name.endswith('.txt'):
                DIRNAME   = root
                DATAPATH  = os.path.join(DIRNAME, name)
                OUTPATH   = os.path.join(DIRNAME, name + ".csv")
                df = pd.read_csv(DATAPATH, delimiter=',')

                for col_label in df.columns:
                    if col_label in DROP_FEATURES:
                        df.drop(col_label, axis=1, inplace=True)

                #change the categorical column to numbers
                df['prev_shift'] = df['prev_shift'].map({'m': 0, 'a': 1, 'e':2})

                #write a csv of numeric data without a header
                df.to_csv(OUTPATH, header= False, index=False)

                print "Wrote dataset of %i instances and %i attributes to %s" % (df.shape + (OUTPATH,))

                with open((root + '/meta.json'), 'w') as f:
                    meta = {'feature_names': FEATURES, 'target_names': LABEL_MAP}
                    json.dump(meta, f, indent=4)
