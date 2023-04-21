# library imports used in our functions
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
from bs4 import BeautifulSoup
import os
import sqlite3
print ("AHAHHAHAHHHHHHH")

# access name & key for the spotify API
cid = 'd590ddaa48094bbe9c51b98dff7dce8f'
secret = 'f72f507876014182a21b26571e60e31e'


# test case data for calc_artists, top10pop, & top10len
birdy = ("Birdy",'spotify:artist:2WX2uTcsvV5OnS0inACecP')
boniver = ("Bon Iver", 'spotify:artist:4LEiUm1SRbFMgfqnQTwUbQ')
kanye = ("Ye",'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x')
jacklarsen = ("Jack Larsen", 'spotify:artist:1UGH6A3IionoSVLLmqtl4o')
bella = ("Ressa", 'spotify:artist:1zwvQUzM8t7zxyKFch91nX')
selena = ("Selena Gomez", 'spotify:artist:0C8ZW7ezQVs4URX5aX7Kqx')
artist_list = (birdy, boniver, kanye, jacklarsen, bella, selena)


# pulls from the spotify api to get an artists top 10 songs by poplarity
# and returns the poplarity scores as a list
# requires the artists spotify UID as a parameter
def top10(art):
    # pulls api request from spotipy library using our key
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    results = spotify.artist_top_tracks(art, country='US')
    
    #cleans data up 
    jason = json.dumps(results)
    data = json.loads(jason)
    
    #parses through data to get popularity score of top 10 songs 
    pop_list = [track['popularity'] for track in data['tracks']]
    len_list = [(track['duration_ms'])//1000 for track in data['tracks']]

    # print ("TOP 10", pop_list)
    # print ("AVG POPULARITY", sum(pop_list)/len(pop_list))

    # returns list of the scores of the 10 most popular songs
    return (pop_list, len_list)


# creates a list of dictionaries, one for each artist with the artists name as the key
# and then a list and average of popularity scores and song lengths
def calc_artists_tuples(artists):
    outlist = []
    for i in range(len(artists)):
        # pop_list = top10pop(artists[i][1])
        # len_list = top10len(artists[i][1])
        tup = top10(artists[i][1])
        print(200-i, "to go")
        len_list = tup[0]
        pop_list = tup[1]
        artist = artists[i][0]
        rank = i + 1
        avpop = sum(pop_list)/len(pop_list)
        avlen = sum(len_list)/len(len_list)
        tuppy = (artist, rank, avpop, avlen)
        
        outlist.append(tuppy)
    return outlist


# creates list of tuples for the top 200 artsists on spotify in the US (artist name, spotify URI)
def get_top_200_artists(html_file):

    # direct path to the static html file
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, html_file)

    with open(full_path, 'r') as f:
        
        # creates a soup to pull from
        soup = BeautifulSoup(f.read(), "html.parser")
        artist_names = soup.find_all("div", class_="styled__Wrapper-sc-135veyd-14 gPJpnT")
        
        # setup stuff
        top_200_artists = []
        prefix = "spotify:artist:"

        # loops through the artists on the top 200 weekly 
        # (from a static html page april 7-13 to avoid violating spotify's no scraping policy) 
        # and pulls their names and spotify URI
        # it then adds the spotify UID prefix to each and makes each artist a tuple (artist name, artist spotify URI)
        # it then returns this as a list of 200 artist tuples 
        for artist in artist_names:
                artist_name = artist.get_text(strip=True)
                artist_link = artist.find("a")["href"]
                code = artist_link.split("/")[-1]
                full_code = prefix + code
                # print("ARTIST:", artist_name)
                # print("SPOTIFY URI:", full_code)
                artist_tuple = (artist_name, full_code)
                top_200_artists.append(artist_tuple)
        # print (top_200_artists)
        return top_200_artists
    

# OLD DATABASE METHOD (ALL AT ONCE)
# sets up a database
def db_setup(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# commits the data from the artist info tuple list to the database
def db_add_data(cur, conn, data):

    # # clears the table spotify_data if it exists and resets it
    # cur.execute("DROP TABLE IF EXISTS spotify_data")
    cur.execute("CREATE TABLE IF NOT EXISTS spotify_data (spotify_rank INTEGER PRIMARY KEY, artist_name TEXT, average_popularity NUMBER, average_length NUMBER)")

    # runs through the top 200 artist list and copies the info in the tuples to the database
    for i in data:
        rank = i[1]
        artist = i[0]
        avpop = i[2]
        avlen = i[3]
        cur.execute("INSERT INTO spotify_data (spotify_rank , artist_name, average_popularity, average_length) VALUES (?,?,?,?)", (rank, artist, avpop, avlen))
        conn.commit()


# NEW DATABSE STUFF (25 AT A TIME, SUPPOSEDLY)
# checks for the last row of the spotify_data database, if database has no data, returns 0
def check_rows_in_db(cur):
    cur.execute('SELECT * FROM spotify_data')
    data  = cur.fetchall()
    if not data:  
        hold = 0
    else:
        hold = data[-1][0]
    return hold


# cursor, connection, full top 200 data, how many rows exist
def add_rows_to_db(cur, conn, data, row):
    max = row + 25
    while row < max:
        if row > 200:
            break
        rank = data[row][1]
        artist = data[row][0]
        avpop = data[row][2]
        avlen = data[row][3]
        cur.execute("INSERT OR IGNORE INTO spotify_data (spotify_rank , artist_name, average_popularity, average_length) VALUES (?,?,?,?)", (rank, artist, avpop, avlen))
        conn.commit()
        row += 1


# essentially a main() for just the databse updates 
def all_db_steps(db_name, data):
    cur, conn = db_setup(db_name)
    cur.execute("CREATE TABLE IF NOT EXISTS spotify_data (spotify_rank INTEGER PRIMARY KEY, artist_name TEXT, average_popularity NUMBER, average_length NUMBER)")
    row = check_rows_in_db(cur)
    add_rows_to_db(cur, conn, data, row)
    cur.close()
    conn.close()


if __name__ == '__main__':

    # # scrape the spotify top 200 chart web page
    top200 = get_top_200_artists("SPOTIFY APRIL 7-13.html")
    # # sss = calc_artists_tuples(artist_list)
    print (top200)
    
    # # makes an api call for each of the top 200 artists and stores the data as a list of tuples
    info = calc_artists_tuples(top200)
    
    # # creates and populates a database with all the data
    # cur, conn = db_setup("spotify_data")
    # # db_add_data(cur, conn, info)
    # row = check_rows_in_db(cur)
    # print(row)
    all_db_steps("spotify_data", info)

    # # print statement to confirm code ran (the api calls take a couple minutes)
    print("DONE RUNNING")