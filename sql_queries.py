# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES


user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY, 
  first_name VARCHAR, 
  last_name VARCHAR, 
  gender CHAR(1) ,
  level VARCHAR NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
  song_id VARCHAR PRIMARY KEY, 
  title VARCHAR NOT NULL, 
  artist_id VARCHAR NOT NULL, 
  year INTEGER, 
  duration NUMERIC
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
  artist_id VARCHAR PRIMARY KEY, 
  name VARCHAR NOT NULL, 
  location VARCHAR, 
  latitude NUMERIC, 
  longitude NUMERIC
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
  start_time TIMESTAMP PRIMARY KEY, 
  hour INTEGER NOT NULL, 
  day INTEGER NOT NULL, 
  week INTEGER NOT NULL, 
  month INTEGER NOT NULL, 
  year INTEGER NOT NULL, 
  weekday varchar NOT NULL
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
  songplay_id SERIAL PRIMARY KEY, 
  start_time TIMESTAMP NOT NULL, 
  user_id INTEGER NOT NULL, 
  level VARCHAR, 
  song_id VARCHAR, 
  artist_id VARCHAR, 
  session_id INTEGER, 
  location VARCHAR, 
  usert_agent VARCHAR,

  CONSTRAINT fk_start_time
   FOREIGN KEY(start_time) 
      REFERENCES time(start_time)
      ON DELETE SET NULL,
  
  CONSTRAINT fk_user_id
   FOREIGN KEY(user_id) 
      REFERENCES users(user_id)
      ON DELETE CASCADE,
  
  CONSTRAINT fk_artist_id
   FOREIGN KEY(artist_id) 
      REFERENCES artists(artist_id)
      ON DELETE SET NULL,
  
  CONSTRAINT fk_song_id
   FOREIGN KEY(song_id) 
      REFERENCES songs(song_id)
      ON DELETE SET NULL
);
""")

# INSERT RECORDS

# COPY migration_helper(profile_id) FROM '{local_auth_filtered_path}' DELIMITER ',' CSV HEADER;
songplay_table_insert = ("""
INSERT INTO songplays (
  start_time,
  user_id,
  level,
  song_id,
  artist_id,
  session_id,
  location,
  usert_agent
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT users_pkey 
      DO UPDATE SET
        (first_name, last_name, gender, level) = (EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.gender, EXCLUDED.level);
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT songs_pkey 
      DO UPDATE SET
        (title, artist_id, year, duration) = (EXCLUDED.title, EXCLUDED.artist_id, EXCLUDED.year, EXCLUDED.duration);
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT artists_pkey 
      DO UPDATE SET
        (name, location, latitude, longitude) = (EXCLUDED.name, EXCLUDED.location, EXCLUDED.latitude, EXCLUDED.longitude);
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT time_pkey 
      DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, songs.artist_id
FROM songs
INNER JOIN artists ON songs.artist_id = artists.artist_id
WHERE LOWER(title) = LOWER(%s) AND LOWER(artists.name) = LOWER(%s) AND duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]