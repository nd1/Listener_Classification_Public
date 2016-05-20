import pandas as pd
from tzwhere import tzwhere
import datetime
import pytz

"""
Take a csv file that contains latitude and longitude info, labeled as 'lat' and 'lon' and add a column with
the timezone identifier. From the timezone identifier, add the time offset with the assumption
it is based on the current time (i.e. do not compensate for regional time shift based on a prior date).

In the event a timezone cannot be determined, reset the NaN value to Australia/Sydney in order to identify
failures in the output file. This option was selected based on our use of North America data.

An initial csv with the lat/ lon data is read in and a final csv is produced with timezone and time offset data.

Created by Nicole Donnelly for Media Organization Capstone team.
"""


def apply_time(input, output):

	tz = tzwhere.tzwhere()
	df = pd.read_csv('xxx.csv')

	df['tzone'] = df[['lat','lon']].apply(lambda x: tz.tzNameAt(x['lat'], x['lon']), axis=1)

	df.fillna(value='Australia/Sydney',inplace=True)

	df['offset'] = df[['tzone']].apply(lambda x: datetime.datetime.now(pytz.timezone(x['tzone'])).strftime('%z'), axis=1)

	df.to_csv(output)
