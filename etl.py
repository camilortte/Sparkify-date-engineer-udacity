import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This functions processes a JSON file with song information, it extracts the artis information and the song data
    information.
    

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file

    RETURNS:
    * None

    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notnull(df), None)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This functions processes a JSON file with song information, it extracts the users information and time information
    information.
    

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file

    RETURNS:
    * None

    """

    # open log file
    df = pd.read_json(filepath, lines=True)
    df = df.where(pd.notnull(df), None)

    # filter by NextSong action
    df = df[ (df.page == "NextSong") & (df.userId.notnull())]

    # Rename columns
    df.rename(columns={'userId' :'user_id', 'firstName': 'first_name', 'lastName': 'last_name'}, inplace=True)

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = {
      'timestamp': df['ts'].values,
      'hour': df['ts'].dt.hour.values,
      'day': df['ts'].dt.day.values, 
      'week_of_year': df['ts'].dt.isocalendar().week.values,  
      'month': df['ts'].dt.month.values,
      'year': df['ts'].dt.year.values,  
      'weekday': df['ts'].dt.weekday .values
    }
    time_df = pd.DataFrame(time_data)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[ ['user_id', 'first_name', 'last_name', 'gender', 'level'] ]

    # Remove null ids
    user_df = user_df[user_df['user_id'].notnull()]

    # insert user records
    for i, row in user_df.iterrows():
        if row.user_id != '' and row.user_id != None:
          cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.user_id, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()