#####################################################
# Imports
#####################################################
import os
import csv
import datetime
import sys
import re
import pytz


#####################################################
# Assignments
#####################################################
"""
datafile location/names
"""
data_dir = 'datafiles'
merged_data = 'entire_dataset.csv'


#####################################################
# Reads all csv files in a folder, parses the data and writes to a consolidated
# file
#####################################################
def process_data(dirname, fwriter):

    count = 0

    for filename in os.listdir(os.path.join(os.getcwd(), data_dir, dirname)):

        count += 1
        print(('Processing started at {0:%m/%d/%Y %H:%M:%S} for file #' +
               '{1:3d} {2:s}').
              format(datetime.datetime.now(pytz.timezone('US/Eastern')),
                     count, filename))
        sys.stdout.flush()

        with open(os.path.join(os.getcwd(), data_dir, dirname, filename),
                  'r') as f:
            try:
                data = csv.reader(f, quoting=csv.QUOTE_NONE)
                for row in data:
                    x = ','.join(row)
                    x = x.replace('xxx', 'station')
                    x = x.split(',')
                    platform = x[9]
                    if platform == '1':
                        platform = 'IPHONE'
                    elif platform == '2':
                        platform = 'ANDROID'
                    elif platform == '3':
                        platform = 'WINDOWPH'
                    fwriter.writerow([x[0], x[1], x[2], x[3], x[4], x[5],
                                      x[6][:x[6].find(' ')],
                                      x[6][x[6].find(' ')+1:len(x[6])],
                                      x[7], x[8], platform, x[10], dirname])
            except csv.Error as e:
                    sys.exit('file {}, line {}: {}'
                             .format(os.path.join(os.getcwd(), dirname,
                                     filename), data.line_num, e))


#####################################################
# Opens an output csv file, calls a function to read all files in a folder &
# consolidates all individual files in one csv file
#####################################################
def merge_all_csv():

    started = datetime.datetime.now(pytz.timezone('US/Eastern'))

    with open(os.path.join(os.getcwd(), data_dir, merged_data), 'w') as csvfile:
        fwriter = csv.writer(csvfile, delimiter=',', quotechar='"',
                             lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(['user', 'piece', 'value', 'interaction', 'elapsed',
                          'duration', 'date', 'time', 'channel', 'origin',
                          'platform', 'piece_type', 'sample_type'])
        try:
            process_data("valid", fwriter)
            process_data("test", fwriter)
            process_data("train", fwriter)

        except csv.Error as a:
            sys.exit('file {}, line {}: {}'
                     .format(merged_data, fwriter.line_num, a))

    ended = datetime.datetime.now(pytz.timezone('US/Eastern'))

    print (("\n\nBegan ... {0:%m/%d/%Y %H:%M:%S}\nEnded ... " +
            "{1:%m/%d/%Y %H:%M:%S}").format(started, ended))


if __name__ == "__main__":
    merge_all_csv()
