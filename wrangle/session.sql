-- Create a list on unique user ID (from the most recent 6 months of user behavior data)

CREATE TABLE unique_users_6month (
  user varchar(15) not null
) ENGINE = innodb

INSERT INTO unique_users_6month
SELECT DISTINCT user
FROM entire_dataset USE INDEX (ind_date)
WHERE Date >= date '2015-09-01'

CREATE INDEX ind_unique_user ON unique_users_6month (user)


-- Store session information in a table

CREATE TABLE sessions (
   user varchar(15),
   date date,
   day tinyint,
   session_id varchar(11),
   session_start datetime,
   session_end datetime,
   duration smallint,
   avg_rating_news float,
   avg_rating_podcast float,
   num_ratings smallint,
   events_s varchar(256),
   events_m varchar(512),
   events_l varchar(4196)
) ENGINE = innodb ROW_FORMAT = DEFAULT;

LOAD DATA LOCAL INFILE 'all.csv' 
INTO TABLE sessions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE INDEX ind_sessions_user ON sessions (user)