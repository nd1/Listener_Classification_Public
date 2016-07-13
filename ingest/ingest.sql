-- Load consolidated user behavior data in a table

CREATE TABLE entire_dataset (
  user varchar(15),
  piece varchar(15),
  rating_value float,
  rating varchar(15),
  elapsed int(11),
  duration int(11),
  channel varchar(15),
  origin varchar(15),
  platform varchar(15),
  thing_type_id int(11),
  date date,
  time time,
  file_set varchar(10)
) ENGINE=InnoDB;


LOAD DATA LOCAL INFILE 'entire_dataset.csv' 
INTO TABLE entire_dataset
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE INDEX ind_user ON entire_dataset (user)

CREATE INDEX ind_date ON entire_dataset (date)

CREATE INDEX ind_user_date ON entire_dataset (user, date)

CREATE INDEX ind_story ON entire_dataset (piece)


-- Load topic data in a table

CREATE TABLE topic_info (
  story_id varchar(16),
  primary_topic varchar(15)
) ENGINE=InnoDB;

LOAD DATA LOCAL INFILE 'topic.csv' 
INTO TABLE topic_info
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE INDEX ind_topic ON topic_info (story_id)
