import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events (
        event_id INT IDENTITY(0,1) PRIMARY KEY,
        artist text,
        auth text,
        first_name text,
        gender text,
        item_in_session int,
        last_name text,
        length float8,
        level text,
        location text,
        method text,
        page text,
        registration text,
        session_id int,
        song_name text,
        status int,
        ts BIGINT,
        user_agent text,
        user_id int)

""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (

        song_id text PRIMARY KEY,
        artist_id text,
        artist_latitude float,
        artist_longitude float,
        artist_location text,
        artist_name text,
        duration float,
        num_songs int,
        title text,
        year int)

""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id INT IDENTITY(0,1) PRIMARY KEY NOT NULL,
        start_time BIGINT NOT NULL,
        user_id int NOT NULL,
        level varchar NOT NULL,
        song_id varchar,
        artist_id varchar,
        session_id int,
        location text,
        user_agent text
    ); 
                    """)

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id int PRIMARY KEY, 
        first_name text NOT NULL, 
        last_name text NOT NULL, 
        gender text,
        level text
    )
                    """)

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id varchar PRIMARY KEY, 
        title text NOT NULL, 
        artist_id varchar NOT NULL, 
        year int, 
        duration float NOT NULL
    )
                    """)

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id varchar PRIMARY KEY,
        name text NOT NULL,
        location text,
        latitude float,
        longitude float
    )
                        """)

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time timestamp PRIMARY KEY NOT NULL,
        weekday varchar(50),
        year int, 
        month int,
        hour int,
        day int, 
        week int     
    )
                    """)

# STAGING TABLES

staging_events_copy = ("""copy staging_events from '{}'
 credentials 'aws_iam_role={}'
 region 'us-west-2' 
 COMPUPDATE OFF STATUPDATE OFF
 JSON '{}'""").format(config.get('S3','LOG_DATA'),
                        config.get('IAM_ROLE', 'ARN'),
                        config.get('S3','LOG_JSONPATH'))


staging_songs_copy = ("""copy staging_songs from '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    COMPUPDATE OFF STATUPDATE OFF
    JSON 'auto'
    """).format(config.get('S3','SONG_DATA'), 
                config.get('IAM_ROLE', 'ARN'))



# FINAL TABLES


songplay_table_insert = ("""
        INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT DISTINCT
        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time,
        e.user_id,
        e.level,
        s.song_id,
        s.artist_id,
        e.session_id,
        e.location,
        e.user_agent
        FROM staging_events_copy e ,staging_songs_copy s
        WHERE e.page = 'NextSong'
        AND e.song_name = s.title
        AND user_id NOT IN (SELECT DISTINCT s.user_id FROM songplays s WHERE s.user_id = user_id
                       AND s.start_time = start_time AND s.session_id = session_id )
 """)



user_table_insert = ("""        
        INSERT INTO users (user_id, first_name, last_name, gender, level)
        SELECT DISTINCT
        user_id,
        first_name,
        last_name,
        gender,
        level
        FROM staging_events_copy e
        WHERE e.page = 'NextSong'
 """)


song_table_insert = ("""
        INSERT INTO songs (song_id,title,artist_id,year,duration)
        SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
        FROM staging_songs s
        WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs)
 """)


artist_table_insert = (""" INSERT INTO artists(artist_id,name,location,latitude,longitude)
        SELECT DISTINCT
        artist_id,
        artist_name,
        location,
        latitude,
        longitude
        FROM staging_songs s
        WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists)
""")
        
        
time_table_insert = ("""INSERT INTO time(start_time,weekday,year,month,hour,day,week)

        SELECT DISTINCT
        start_time,
        EXTRACT(weekday FROM start_time) As weekday,
        EXTRACT(year FROM start_time) As year,
        EXTRACT(month FROM start_time) As month,
        EXTRACT(hour FROM start_time) As hour,
        EXTRACT(day FROM start_time) As day,
        EXTRACT(week FROM start_time) As week
        FROM (SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' AS start_time FROM staging_events s)
 """)

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

## https://knowledge.udacity.com/questions/47005
## https://knowledge.udacity.com/questions/144884
## https://knowledge.udacity.com/questions/214736
## https://knowledge.udacity.com/questions/141440