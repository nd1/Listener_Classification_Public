#####################################################
# Imports
#####################################################
import csv
import datetime
import sys
import os
import pytz
import mysql.connector
from pandas import DataFrame
from switchers import *


#####################################################
# Assignments
#####################################################
"""
datafile location/names
"""
data_dir = 'datafiles'
unique_users_file = 'unique_users_6month_rest.csv'
out_file = 'rest.csv'
"""
no. of users whose behavior data is retrieved (at a time) from MySQL database
"""
chunk = 100
"""
max no. of seconds between end_time and start_time of two individual contents
assumed to be consecutive
"""
gap = 10
"""
static portion of the sql code
"""
sql_str_base = ("select user, date, dayofweek(date) as day, rating, " +
                "to_seconds(time), elapsed, rating_value, " +
                "thing_type_id, origin, platform, case rating " +
                "when 'COMPLETED' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) - elapsed " +
                "when 'SKIP' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) - elapsed " +
                "when 'THUMBUP' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) - elapsed " +
                "when 'START' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'SHARE' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) - elapsed " +
                "when 'SRCHSTART' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'SRCHCOMPL' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) - elapsed " +
                "else 0  " +
                "end as start_time, " +
                "case rating " +
                "when 'COMPLETED' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'SKIP' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'THUMBUP' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'START' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) + elapsed " +
                "when 'SHARE' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "when 'SRCHSTART' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) + elapsed " +
                "when 'SRCHCOMPL' then timestampdiff(second,'1970-01-01',concat(date, ' ', time)) " +
                "else 0 " +
                "end as end_time " +
                "from entire_dataset use index (ind_user_date) " +
                "where date >= date '2015-09-01' and user in ( ")


#####################################################
# Assigns single-letter code for the rating of individual contents by the users
#####################################################
"""
output example: c, k, t
"""
def events_s_code(df, i):
    return rate_code(df.iloc[i]['rating'])


#####################################################
# Builds 2-letter code for each individual content listened by the user
#####################################################
"""
1st letter: rating of the individual contents
2nd letter: short-form content (e.g. news) or long-form content (e.g. podcast)
output example: cN, tP, kN, kP
"""
def events_m_code(df, i):
    return (events_s_code(df, i) +
            content_type_code(df.iloc[i]['thing_type_id']))


#####################################################
# Builds 4-letter code for each individual content listened by the user
#####################################################
"""
1st letter: device platform (e.g. iOS, Android)
2nd letter: origin of the content (e.g. archives, break, lead, featured)
3rd letter: rating of the individual contents
4th letter: short-form content (e.g. news) or long-form content (e.g. podcast)
output example: 1acN, 2btP, 1okN, 3ckP
"""
def events_l_code(df, i):
    return (platform_code(df.iloc[i]['platform']) +
            origin_code(df.iloc[i]['origin']) +
            events_m_code(df, i))


#####################################################
# Writes session data to a .csv file
#####################################################
def write_file(f, user, date, day, session_num,
               session_start, session_end, events_s, events_m, events_l,
               sum_rating_news, sum_rating_podcast):
    duration = session_end - session_start
    num_news = events_m.count('N')
    if num_news == 0:
        avg_rating_news = 0
    else:
        avg_rating_news = sum_rating_news / num_news
    num_podcast = events_m.count('P')
    if num_podcast == 0:
        avg_rating_podcast = 0
    else:
        avg_rating_podcast = sum_rating_podcast / num_podcast
    if duration > 0:
        f.writerow([user, str(date), day,
                    (str(date)+('00'+str(session_num))[-2:]).replace('-', ''),
                    datetime.datetime.utcfromtimestamp(int(session_start)),
                    datetime.datetime.utcfromtimestamp(int(session_end)),
                    duration, avg_rating_news, avg_rating_podcast,
                    len(events_s), events_s, events_m, events_l])


#####################################################
# Creates listening sessions
# Warning: complicated code logic
#####################################################
"""
steps of calculations (high-level):
1:  for the "current" day, create a dataframe that holds all attributes of the
    contents listened during the day
2:  create start and end time for each individual content
3:  if there is only one content listened in a day, start time & end time of
    the content define the session
4: if there are more than 1 content listened in a day
   a:   adjust start and end time of each content, if needed (note: start and
        end time of a content is calculated from "elapsed" time;
        the assumptions made in handling the "elapsed" time for certain user
        ratings may generate anomalous start and end time of a content so
        adjustments may be needed to overcome calculation anomalies)
        1:  set start time of a content = end time of the previous content
        2:  set end time of a content = end time of the previous content
   b: caculate the gap, i.e., time diff between end time of a content and the
      start time of the following content. if the gap < "gap" then "session"
      continues with the following content. otherwise, "session" ends.
"""
def make_sessions_for_a_day(df, u, dates, d, fwriter, users):

    # initialization
    session_num = 1
    events_s = events_m = events_l = ""
    sum_rat_val_n = sum_rat_val_p = 0
    df2 = df[df.date == dates[d]]
    num_data = len(df2.index)
    start_time = []
    end_time = []

    for j in range(0, num_data):
        start_time.append(df2.iloc[j]['start_time'])
        end_time.append(df2.iloc[j]['end_time'])

    start_t = start_time[0]
    end_t = end_time[0]

    if num_data == 1:  # only one content listened in a day
        events_s += events_s_code(df2, 0)
        events_m += events_m_code(df2, 0)
        events_l += events_l_code(df2, 0)
        if df2.iloc[0]['thing_type_id'] == 1:
            sum_rat_val_n += df2.iloc[0]['rating_value']
        elif df2.iloc[0]['thing_type_id'] == 15:
            sum_rat_val_p += df2.iloc[0]['rating_value']
        write_file(fwriter, users[u], dates[d], df2.iloc[0]['day'],
                   session_num, start_t, end_t, events_s, events_m, events_l,
                   sum_rat_val_n, sum_rat_val_p)
    else:  # more than one content listened in a day
        for j in range(1, num_data):  # adjust start and end time, if needed
            if start_time[j] < end_time[j-1]:
                start_time[j] = end_time[j-1]
            if end_time[j] < end_time[j-1]:
                end_time[j] = end_time[j-1]
        for j in range(1, num_data):
            if start_time[j] > end_time[j-1] + gap:  # session ends
                events_s += events_s_code(df2, j-1)
                events_m += events_m_code(df2, j-1)
                events_l += events_l_code(df2, j-1)
                if df2.iloc[j-1]['thing_type_id'] == 1:
                    sum_rat_val_n += df2.iloc[j-1]['rating_value']
                elif df2.iloc[j-1]['thing_type_id'] == 15:
                    sum_rat_val_p += df2.iloc[j-1]['rating_value']
                write_file(fwriter, users[u], dates[d], df2.iloc[j-1]['day'],
                           session_num, start_t, end_t, events_s, events_m,
                           events_l, sum_rat_val_n, sum_rat_val_p)
                events_s = events_m = events_l = ""  # init for next session
                sum_rat_val_n = sum_rat_val_p = 0
                start_t = start_time[j]
                end_t = end_time[j]
                session_num += 1
            else:
                end_t = end_time[j]  # "session" continues
                events_s += events_s_code(df2, j-1)
                events_m += events_m_code(df2, j-1)
                events_l += events_l_code(df2, j-1)
                if df2.iloc[j-1]['thing_type_id'] == 1:
                    sum_rat_val_n += df2.iloc[j-1]['rating_value']
                elif df2.iloc[j-1]['thing_type_id'] == 15:
                    sum_rat_val_p += df2.iloc[j-1]['rating_value']
        else:
            events_s += events_s_code(df2, j)  # last "session" of a day
            events_m += events_m_code(df2, j)
            events_l += events_l_code(df2, j)
            if df2.iloc[j]['thing_type_id'] == 1:
                sum_rat_val_n += df2.iloc[j]['rating_value']
            elif df2.iloc[j]['thing_type_id'] == 15:
                sum_rat_val_p += df2.iloc[j]['rating_value']
            write_file(fwriter, users[u], dates[d], df2.iloc[j]['day'],
                       session_num, start_t, end_t, events_s, events_m,
                       events_l, sum_rat_val_n, sum_rat_val_p)


#####################################################
# Create list of unique users from input file
#####################################################
def get_unique_users(unique_users):
    with open(os.path.join(os.getcwd(), data_dir,
              unique_users_file), 'r') as f:
        freader = csv.reader(f, delimiter=',', quotechar='"',
                             lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        try:
            next(freader)
            for row in freader:
                unique_users.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(f, f.line_num, e))


#####################################################
# Complete sql code dynamically by adding list of users
#####################################################
def build_sql(sql_str, max_iter, iter, users):

    blksize = chunk
    if iter == max_iter:
        blksize = len(users) - (max_iter - 1) * chunk

    str_sql = sql_str
    for i in range(0, blksize):
        str_sql += ("'" + str(users[(iter - 1) * chunk + i])
                    .strip("'[]'") + "', ")
    str_sql = str_sql[:-2] + ")"
    return str_sql


#####################################################
# main/do_sessions
#####################################################
def do_sessions():
    """
    initialization
    """
    started = datetime.datetime.now(pytz.timezone('US/Eastern'))
    unique_users = []

    db = mysql.connector.connect(host="",
                                 user="",
                                 passwd="",
                                 db="")
    cur = db.cursor()

    get_unique_users(unique_users)
    print('\n\nThere are {0:8,d} unique users\n'.format(len(unique_users)))

    max_iter = int(len(unique_users)/chunk) + 1
    iter = 1

    with open(os.path.join(os.getcwd(), data_dir, out_file), 'w') as o:
        fwriter = csv.writer(o, delimiter=',', quotechar='"',
                             lineterminator='\n',
                             quoting=csv.QUOTE_MINIMAL)
        try:
            fwriter.writerow(['user', 'date', 'day', 'session_id',
                              'session_start', 'session_end', 'duration',
                              'avg_rating_news', 'avg_rating_podcast',
                              'num_ratings', 'events_short', 'events_medium',
                              'events_long'])
            while iter <= max_iter:  # loop over one chunk at a time
                print (('Iteration {0:6,d} of {1:6,d} started ' +
                       "{2:%m/%d/%Y %H:%M:%S}").format(iter, max_iter,
                       datetime.datetime.now(pytz.timezone('US/Eastern'))))
                sys.stdout.flush()
                """
                get behavior data from MySQL database
                """
                sql_str = sql_str_base
                cur.execute(build_sql(sql_str, max_iter, iter, unique_users))
                df = DataFrame(cur.fetchall())  # behavior data in dataframe

                if len(df.index) > 0:  # found data in database
                    df.columns = ['user', 'date', 'day', 'rating', 'time',
                                  'elapsed', 'rating_value', 'thing_type_id',
                                  'origin', 'platform', 'start_time',
                                  'end_time']
                    df = df.sort_values(['user', 'date', 'start_time'],
                                        ascending=[True, True, True])
                    users = list(set(df['user']))  # unique users from query
                    if chunk != len(users):  # potential error trap
                        print (('Query found only {0:4,d} users instead of ' +
                               'expected {1:4,d} users')
                               .format(len(users), chunk))
                    for u in range(len(users)):  # loop for an user
                        df1 = df[df.user == users[u]]
                        dates = list(set(df1['date']))
                        dates.sort()
                        for d in range(len(dates)):  # loop for day & an user
                            """
                            sessions for user & day combo
                            """
                            make_sessions_for_a_day(df1, u, dates, d, fwriter,
                                                    users)
                else:  # error trap
                    print 'Query had no output'
                    sys.stdout.flush()
                iter += 1
        except csv.Error as c:
            sys.exit('file {}, line {}: {}'.format(o, o.line_num, c))

    """
    cleanup
    """
    db.close()

    ended = datetime.datetime.now(pytz.timezone('US/Eastern'))

    print (("\n\nBegan ... {0:%m/%d/%Y %H:%M:%S}\nEnded ... " +
           "{1:%m/%d/%Y %H:%M:%S}").format(started, ended))


if __name__ == "__main__":
    do_sessions()
