from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
from bs4 import BeautifulSoup
import os
import sqlite3
import requests

def setup_spotify():
    # Set up the Spotipy client with appropriate authentication credentials
    cid = 'd590ddaa48094bbe9c51b98dff7dce8f'
    secret = 'f72f507876014182a21b26571e60e31e'

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, 
                                                   client_secret=secret))
    return sp

def create_database():
    # Create a SQLite database and table to store the playlist data
    conn = sqlite3.connect('billboard_songs.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            rank INT,
            song_title TEXT,
            artist_name TEXT
        )
    ''')

    conn.commit()
    return conn, c

def insert_playlist_data(playlist_id, sp, c):
    # Use the Spotipy client to retrieve the playlist data and store it in the database
    offset = 0
    limit = 25
    count = 1

    while offset < 100:
        results = sp.playlist_items(playlist_id,
                                     offset=offset,
                                     limit=limit,
                                     additional_types=['track'])

        for i, item in enumerate(results["items"]):
            track = item["track"]
            artists = ", ".join([artist["name"] for artist in track["artists"]])
            
            c.execute("INSERT INTO songs (rank, song_title, artist_name) VALUES (?, ?, ?)", (count, track['name'], artists))
            count += 1

        conn.commit()
        offset += limit
        if offset >= 100:
            break
        elif offset + limit > 100:
            limit = 100 - offset

if __name__ == '__main__':
    sp = setup_spotify()
    conn, c = create_database()
    playlist_id = '6UeSakyzhiEt4NB3UAd6NQ' # billboard hot 100 playlist
    insert_playlist_data(playlist_id, sp, c)
    conn.close()

    conn = sqlite3.connect('billboard_songs.db')
    c = conn.cursor()

    # Create a new table to hold artist counts
    conn.execute('''
        CREATE TABLE artist_counts (
            artist_name TEXT,
            count INT
        );
    ''')

    c.execute("SELECT artist_name FROM songs")
    artists_list = [artist for row in c.fetchall() for artist in row[0].split(', ')]

    # Create a dictionary to hold the artist names and their counts
    artist_counts = {}

    # Count the number of appearances for each artist
    for artist in artists_list:
        if artist in artist_counts:
            artist_counts[artist] += 1
        else:
            artist_counts[artist] = 1

    # Insert the artist names and counts into the artist_counts table
    for artist, count in artist_counts.items():
        c.execute("INSERT INTO artist_counts (artist_name, count) VALUES (?, ?)", (artist, count))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()