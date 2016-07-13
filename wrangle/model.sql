-- Chain sessions to identify previous and current session characteristics

CREATE TABLE chain_intermediate (
   user varchar(15),
   prev_date date,
   next_date date,
   prev_session_id varchar(11),
   next_session_id varchar(11),
   duration smallint,
   prev_num_ratings smallint,
   prev_events_s varchar(256),
   prev_events_m varchar(512),
   prev_events_l varchar(4196),
   prev_session_start datetime,
   prev_session_end datetime,
   prev_avg_rating_news float,
   prev_avg_rating_podcast float
) ENGINE = innodb ROW_FORMAT = DEFAULT;

INSERT INTO chain_intermediate
SELECT a.user as user, a.date as prev_date, min(b.date) as next_date, 
a.session_id as prev_session_id, min(b.session_id) as next_session_id,
a.duration as prev_duration, a.num_ratings as prev_num_ratings, 
a.events_s as prev_events_s, a.events_m as prev_events_m, 
a.events_l as prev_events_l, a.session_start as prev_session_start, 
a.session_end as prev_session_end,
a.avg_rating_news as prev_avg_rating_news,
a.avg_rating_podcast as prev_avg_rating_podcast
FROM sessions AS a USE INDEX (ind_sessions_user)
JOIN sessions AS b USE INDEX (ind_sessions_user) ON
a.user=b.user and b.session_start > a.session_end
GROUP BY a.user, a.date, a.session_id, a.duration, a.num_ratings, a.events_s, 
a.events_m, a.events_l, a.session_start, a.session_end, a.avg_rating_news, 
a.avg_rating_podcast

CREATE INDEX ind_chain_user ON chain_intermediate (user)

CREATE TABLE session_chain (
   user varchar(15),
   prev_session_id varchar(11),
   next_session_id varchar(11),
   prev_duration smallint,
   next_duration smallint,
   prev_num_ratings smallint,
   next_num_ratings smallint,
   prev_avg_rating_news float,
   prev_avg_rating_podcast float,
   next_avg_rating_news float,
   next_avg_rating_podcast float,
   prev_shift varchar(2),
   next_shift varchar(2),
   prev_num_news smallint,
   prev_num_podcast smallint,
   next_num_news smallint,
   next_num_podcast smallint,
   prev_platform varchar(2),
   next_platform varchar(2),
   prev_num_complete smallint,
   prev_num_thumbup smallint,
   prev_num_skip smallint,
   prev_num_searchcomplete smallint,
   next_num_complete smallint,
   next_num_thumbup smallint,
   next_num_skip smallint,
   next_num_searchcomplete smallint,
   time_diff_hr float
) ENGINE = innodb ROW_FORMAT = DEFAULT;

INSERT INTO session_chain
SELECT a.user, a.prev_session_id, a.next_session_id,
a.duration as prev_duration, b.duration as next_duration, a.prev_num_ratings, 
b.num_ratings as next_num_ratings, 
a.prev_avg_rating_news, a.prev_avg_rating_podcast, 
b.avg_rating_news as next_avg_rating_news, 
b.avg_rating_podcast as next_avg_rating_podcast,
if(time(prev_session_start) between '05:00:00' and '11:00:00', 'm', 
if (time(prev_session_start) between '11:00:00' and '19:00:00', 'a', 'e')) as prev_shift,
if(time(b.session_start) between '05:00:00' and '11:00:00', 'm', 
if (time(b.session_start) between '11:00:00' and '19:00:00', 'a', 'e')) as next_shift,
(length(a.prev_events_m)-length(replace(a.prev_events_m, 'N', ''))) as prev_num_news,
(length(a.prev_events_m)-length(replace(a.prev_events_m, 'P', ''))) as prev_num_podcast,
(length(b.events_m)-length(replace(b.events_m, 'N', ''))) as next_num_news,
(length(b.events_m)-length(replace(b.events_m, 'P', ''))) as next_num_podcast,
substring(a.prev_events_l,1,1) as prev_platform,
substring(b.events_l,1,1) as next_platform,
(length(a.prev_events_s)-length(replace(a.prev_events_s, 'c', ''))) as prev_num_complete,
(length(a.prev_events_s)-length(replace(a.prev_events_s, 't', ''))) as prev_num_thumbup,
(length(a.prev_events_s)-length(replace(a.prev_events_s, 'k', ''))) as prev_num_skip,
(length(a.prev_events_s)-length(replace(a.prev_events_s, 'l', ''))) as prev_num_searchcomplete,
(length(b.events_s)-length(replace(b.events_s, 'c', ''))) as next_num_complete,
(length(b.events_s)-length(replace(b.events_s, 't', ''))) as next_num_thumbup,
(length(b.events_s)-length(replace(b.events_s, 'k', ''))) as next_num_skip,
(length(b.events_s)-length(replace(b.events_s, 'l', ''))) as next_num_searchcomplete,
(time_to_sec(b.session_start) - time_to_sec(a.prev_session_end))/3600 as time_diff_hr
FROM Chain_intermediate AS a USE INDEX (ind_chain_user) 
JOIN sessions as b USE INDEX (ind_sessions_user)
on a.user = b.user and b.session_id = a.next_session_id

CREATE TABLE session_chain_ML_Final (
   user varchar(15),
   prev_session_id varchar(11),
   next_session_id varchar(11),
   prev_duration smallint,
   next_duration smallint,
   prev_num_ratings smallint,
   next_num_ratings smallint,
   prev_avg_rating_news float,
   prev_avg_rating_podcast float,
   next_avg_rating_news float,
   next_avg_rating_podcast float,
   prev_shift varchar(2),
   next_shift varchar(2),
   prev_num_news smallint,
   prev_num_podcast smallint,
   next_num_news smallint,
   next_num_podcast smallint,
   prev_platform varchar(2),
   next_platform varchar(2),
   prev_num_complete smallint,
   prev_num_thumbup smallint,
   prev_num_skip smallint,
   prev_num_searchcomplete smallint,
   next_num_complete smallint,
   next_num_thumbup smallint,
   next_num_skip smallint,
   next_num_searchcomplete smallint,
   time_diff_hr float,
   target smallint
) ENGINE = innodb ROW_FORMAT = DEFAULT;

INSERT INTO session_chain_ML_Final
SELECT *, if(next_num_podcast = 0, 0, 1) as target
FROM session_chain
