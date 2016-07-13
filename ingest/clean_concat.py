import os
import pandas as pd
import glob
from timeit import default_timer

"""
Concatenate all csv files in a directory into one data frame and write that data frame to a csv.

This script assumes all files are of a known file name and file format.

File name format = <data set type>_yyyy-mm_#.csv

File format is a csv with the following fields: 'user_id', 'story_id', 'rating_value', 'rating', 'elapsed', 'duration', 'timestamp', 'channel', 'thing_type_id'

The clean_data function parses 'timestamp' into separate date and time columns. It then appends a column called 'file_set' with data set type name (train, test, or valid).

clean_data then removes instances of the data source name from the data and replaces them with the string 'station'.

 Written by Nicole Donnelly for the Media Organization capstone team.
"""

def clean_data(full_name):

	file_name = os.path.basename(full_name)
	file_set = file_name[0:(len(file_name) - 14)]

	df = pd.read_csv(full_name, header=None, names=['user_id', 'story_id', 'value', 'interaction', 'elapsed', 'duration', 'timestamp', 'channel', 'thing_type_id'], parse_dates=['timestamp'], infer_datetime_format=True)

	temp = pd.DatetimeIndex(df['timestamp'])
	df['date'] = temp.date
	df['time'] = temp.time
	del df['timestamp']

	df['file_set'] = file_set

	df['channel'].replace('xxx','station',inplace=True)

	#code to deal with NaN values?

	return df


def concatentate_all(path, output):

	start = default_timer()

	all_files = glob.glob(os.path.join(path, "*.csv"))
	df = pd.concat((clean_data(f) for f in all_files), ignore_index=True)

	df.to_csv(output)
	duration = default_timer() - start
	print duration
