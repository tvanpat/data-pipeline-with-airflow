class SqlQueries:
    
    songplays_table_insert = ("""
    (
    start_time,
    user_id, 
    level,
    song_id,
    artist_id,
    session_id, 
    location, 
    user_agent)
    SELECT DISTINCT se.ts as start_time,
                se.userid as user_id,
                se.level as level,
                ss.song_id as song_id,
                ss.artist_id as artist_id,
                se.sessionid as session_id,
                se.location as location,
                se.useragent as user_agent
    FROM staging_events se
    JOIN staging_songs ss ON se.song=ss.title AND se.artist = ss.artist_name
""")


    users_table_insert = ("""
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    songs_table_insert = ("""
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artists_table_insert = ("""
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""(start_time, hour, day, week, month, year, weekday)
    SELECT distinct ts,
                EXTRACT(hour from ts),
                EXTRACT(day from ts),
                EXTRACT(week from ts),
                EXTRACT(month from ts),
                EXTRACT(year from ts),
                EXTRACT(weekday from ts)
    FROM staging_events
    WHERE ts IS NOT NULL;
    """)

