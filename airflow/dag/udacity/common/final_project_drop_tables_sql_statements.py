staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs;"
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
songsplay_table_drop      = "DROP TABLE IF EXISTS songsplay;"
users_table_drop          = "DROP TABLE IF EXISTS users;"
songs_table_drop          = "DROP TABLE IF EXISTS songs;"
artists_table_drop        = "DROP TABLE IF EXISTS artists;"
time_table_drop           = "DROP TABLE IF EXISTS time;"

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songsplay_table_drop, users_table_drop, songs_table_drop, artists_table_drop, time_table_drop]
