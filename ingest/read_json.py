#####################################################
# Imports
#####################################################
import csv
import datetime
import sys
import pytz
import json
import os


#####################################################
# Assignments
#####################################################
"""
datafile location/names
"""
data_dir = 'datafiles'
topic_data = 'topic.csv'
json_data_file = 'topics_by_story_id.json'


#####################################################
# Converts a json file to csv for loading onto a MySQL database
#####################################################
def json_to_csv():

	started = datetime.datetime.now(pytz.timezone('US/Eastern'))

	with open(os.path.join(os.getcwd(), data_dir, json_data_file), 'r') as j_file:
		 json_data = json.load(j_file)
		 with open(os.path.join(os.getcwd(), data_dir, topic_data), 'w') as f:
			fwriter = csv.writer(f, delimiter=',', quotechar='"',
								 lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
			fwriter.writerow(['story_id', 'primary_topic'])
			try:
				for i in range(len(json_data)):
					fwriter.writerow([json_data[i]['story_id'],
								  	  json_data[i]['primary']])
			except csv.Error as e:
				sys.exit('file {}, line {}: {}'.format(f, f.line_num, e))

	ended = datetime.datetime.now(pytz.timezone('US/Eastern'))

	print (("\n\nBegan ... {0:%m/%d/%Y %H:%M:%S}\nEnded ... " +
	            "{1:%m/%d/%Y %H:%M:%S}").format(started, ended))


if __name__ == "__main__":
	json_to_csv()
