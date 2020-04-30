# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_fact"
user_table_drop = "DROP TABLE IF EXISTS user_dim"
song_table_drop = "DROP TABLE IF EXISTS song_dim"
artist_table_drop = "DROP TABLE IF EXISTS artist_dim"
time_table_drop = "DROP TABLE IF EXISTS time_dim"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events(
artist          VARCHAR,
auth            VARCHAR,
firstName       VARCHAR,
gender          VARCHAR,
itemInSession   INTEGER,
lastName       VARCHAR,
length          NUMERIC,
level           VARCHAR,
location        VARCHAR,
method          VARCHAR,
page            VARCHAR,
registration    BIGINT,
sessionId       INTEGER,
song            VARCHAR,
status          INTEGER,
ts              TIMESTAMP,
userAgent       VARCHAR,
userId          INTEGER
);
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
    artist_id VARCHAR,
    artist_latitude NUMERIC,
    artist_location VARCHAR,
    artist_longitude NUMERIC,
    artist_name VARCHAR,
    duration FLOAT,
    num_songs INTEGER,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER
);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_dim(
user_id INTEGER DISTKEY,
first_name VARCHAR,
last_name VARCHAR,
gender VARCHAR,
level VARCHAR,
PRIMARY KEY(user_id)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song_dim(
song_id VARCHAR,
title VARCHAR,
artist_id VARCHAR,
year INTEGER,
duration NUMERIC,
PRIMARY KEY (song_id)
);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist_dim(
artist_id VARCHAR,
name VARCHAR,
location VARCHAR,
latitude NUMERIC,
longitude NUMERIC,
PRIMARY KEY (artist_id)
);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_dim(
start_time TIMESTAMP,
hour INTEGER,
day INTEGER,
week INTEGER,
month INTEGER,
year INTEGER,
weekday INTEGER,
PRIMARY KEY(start_time)
);
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_fact(
songplay_id          INTEGER IDENTITY(0,1)  sortkey,
start_time          TIMESTAMP,
user_id              INTEGER,
level                VARCHAR,
song_id              VARCHAR,
artist_id            VARCHAR,
session_id           INTEGER,
location             VARCHAR,
user_agent           VARCHAR,
PRIMARY KEY (songplay_id)
);
""")

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        user_table_create, artist_table_create, song_table_create,  time_table_create, songplay_table_create]
