staging_songs_table_create = ("""
    CREATE TABLE "staging_songs" (
        "num_songs"        INT,            
        "artist_id"        TEXT,
        "artist_latitude"  DECIMAL(10, 8),
        "artist_longitude" DECIMAL(11, 8),
        "artist_location"  TEXT,
        "artist_name"      TEXT,
        "song_id"          TEXT,
        "title"            TEXT,
        "duration"         DOUBLE PRECISION,
        "year"             SMALLINT
    );
""")

staging_events_table_create= ("""
    CREATE TABLE "staging_events" (
        "artist"        TEXT,
        "auth"          VARCHAR(15),
        "firstName"     VARCHAR(25),
        "gender"        CHAR(1),
        "itemInSession" INT,
        "lastName"      VARCHAR(25),
        "length"        DOUBLE PRECISION,
        "level"         VARCHAR(10),
        "location"      TEXT,
        "method"        VARCHAR(4),
        "page"          VARCHAR(25),
        "registration"  DOUBLE PRECISION,
        "sessionId"     INT,
        "song"          TEXT,
        "status"        CHAR(3), 
        "ts"            TIMESTAMP,
        "userAgent"     TEXT,
        "userId"        INT
    );
""")

artists_table_create = ("""
    CREATE TABLE "artists" (
        "a_id"        TEXT           NOT NULL SORTKEY,
        "a_name"      TEXT           NOT NULL,
        "a_latitude"  DECIMAL(10, 8),
        "a_longitude" DECIMAL(11, 8),
        "a_location"  TEXT,
        PRIMARY KEY (a_id)
    );
""")

songs_table_create = ("""
    CREATE TABLE "songs" (
            "s_id"       TEXT NOT NULL SORTKEY DISTKEY,
            "s_title"    TEXT NOT NULL,
            "s_duration" REAL,
            "s_year"     SMALLINT NOT NULL,
            "s_artistId" TEXT NOT NULL,
            PRIMARY KEY (s_id),
            FOREIGN KEY (s_artistId) REFERENCES artists(a_id)
    );
""")

users_table_create = ("""
    CREATE TABLE "users" ( 
        "u_id"           INT              NOT NULL SORTKEY,
        "u_firstName"    VARCHAR(25)      NOT NULL,
        "u_lastName"     VARCHAR(25)      NOT NULL, 
        "u_gender"       CHAR(1)          NOT NULL,
        "u_level"        VARCHAR(10)      NOT NULL,
        PRIMARY KEY (u_id)
    );
""")

time_table_create = ("""
    CREATE TABLE "time" (
        "t_startDateTime" TIMESTAMP NOT NULL SORTKEY,
        "t_year"          SMALLINT NOT NULL,
        "t_month"         SMALLINT NOT NULL,
        "t_week"          SMALLINT NOT NULL,
        "t_day"           SMALLINT NOT NULL,
        "t_hour"          SMALLINT NOT NULL,
        PRIMARY KEY (t_startDateTime)
    );
""")

songsplay_table_create = ("""
    CREATE TABLE "songsplay" (
        "sp_id"            INT IDENTITY(0,1) NOT NULL,
        "sp_songId"        TEXT              NOT NULL DISTKEY,
        "sp_artistId"      TEXT              NOT NULL,
        "sp_userId"        INT               NOT NULL,
        "sp_timeId"        TIMESTAMP         NOT NULL SORTKEY,
        "sp_length"        DOUBLE PRECISION  NOT NULL,
        "sp_location"      TEXT              NOT NULL,
        "sp_agent"         TEXT              NOT NULL,
        PRIMARY KEY (sp_id),
        FOREIGN KEY (sp_songId)   REFERENCES songs(s_id),
        FOREIGN KEY (sp_userId)   REFERENCES users(u_id),
        FOREIGN KEY (sp_artistId) REFERENCES artists(a_id),
        FOREIGN KEY (sp_timeID)   REFERENCES time(t_startDateTime)
    );
""")

create_table_queries = [staging_events_table_create, staging_songs_table_create, artists_table_create, songs_table_create, users_table_create, time_table_create, songsplay_table_create]
