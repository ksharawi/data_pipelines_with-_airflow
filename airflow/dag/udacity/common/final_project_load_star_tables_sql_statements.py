songsplay_table_insert = ("""
    INSERT INTO songsplay (sp_songId, sp_artistId, sp_userId, sp_timeId, sp_length, sp_location, sp_agent)
        SELECT ss.song_id, ss.artist_id, se.userId, se.ts, se.length, se.location, se.userAgent
        FROM staging_events se
        JOIN staging_songs ss ON se.song = ss.title and se.artist = ss.artist_name
        WHERE se.page !='Home'
    ;
""")

users_table_insert = ("""
    INSERT INTO users (u_id, u_firstName, u_lastName, u_gender, u_level)
        SELECT DISTINCT userId, firstName, lastName, gender, level
        FROM staging_events
        WHERE userId IS NOT NULL
    ;
""")

songs_table_insert = ("""
    INSERT INTO songs (s_id, s_title, s_duration, s_year, s_artistId)
        SELECT DISTINCT song_id, title, duration, year, artist_id
        FROM staging_songs
        WHERE song_id IS NOT NULL
    ;
""")

artists_table_insert = ("""
    INSERT INTO artists (a_id, a_name, a_latitude, a_longitude, a_location)
        SELECT DISTINCT artist_id, artist_name, artist_latitude, artist_longitude, artist_location
        FROM staging_songs
        WHERE artist_id IS NOT NULL
    ;
""")

time_table_insert = ("""
    INSERT INTO time (t_startDateTime, t_year, t_month, t_week, t_day, t_hour)
        SELECT DISTINCT ts, EXTRACT (year FROM ts), EXTRACT (month FROM ts), EXTRACT (week FROM ts), EXTRACT (day FROM ts), EXTRACT (hour FROM ts)
        FROM staging_events se
        JOIN staging_songs ss ON se.song = ss.title and se.artist = ss.artist_name
        WHERE page !='Home' 
    ;
""")

insert_table_queries = [artists_table_insert, songs_table_insert, users_table_insert, time_table_insert, songsplay_table_insert]
