# library imports used in our functions
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
from bs4 import BeautifulSoup
import os
import sqlite3
import requests

print ("AHAHHAHAHHHHHHH HELPPPPPPPPPPPP")

# access name & key for the spotify API
cid = "5fe9f1a3a7e745d986a9ff911c4aa164"
secret = "9fab9dcc267845889aaf3a4cbffa7899"


# pulls from the spotify api to get an artists top 10 songs by poplarity
# and returns the poplarity scores as a list
# requires the artists spotify UID as a parameter
def top10(art):
    # pulls api request from spotipy library using our key
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    results = spotify.artist_top_tracks(art, country='US') # CURRENTLY NOT FUNCTIONING, NOT ON OUR END
    
    #cleans data up 
    jason = json.dumps(results)
    data = json.loads(jason)
    
    #parses through data to get popularity score of top 10 songs 
    pop_list = [track['popularity'] for track in data['tracks']]
    len_list = [(track['duration_ms'])//1000 for track in data['tracks']]

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


# creates list of tuples for the top 200 artsists on spotify in the US (artist name, spotify URI)
# directly by using a get request from spotify's website (instesd of parsing the static html file)
# This code is correct to directly scrape from spotify's top 200 chart, 
# but because spotify requires you to log in with your own spotify account and password,
# the request lacks the permissions to execute. We still wanted to use the spotify top 200 list because
# a) it is the most accurate to use in conjunction with the spotify API and 
# b) the difference between scraping directly vs the static html is minimal and
# c) we wrote code to prove we know how to scrape directly from the site despite that not being what we actually ended up doing.
def get_top_200_artists_direct(url):
    
    r = requests.get(url)
    # check if request worked
    if r.status_code == 200:
        html_file = r.text     
    else:
        print('FAIL :(')

    soup = BeautifulSoup(html_file, "html.parser")
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
        
# sets up a database
def db_setup(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    conn.commit()
    return cur, conn

#################################################################################
# ATTEMPT TO ADD 25 LINES AT A TIME, WAS UNSUCCESSFUL, BUT WANTED TO SHOW OUR THOUGHT PROCESS

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


#################################################################################

if __name__ == '__main__':

    # scrape the spotify top 200 chart web page
    top200 = get_top_200_artists("SPOTIFY APRIL 7-13.html")
    # top200 = get_top_200_artists_direct("https://charts.spotify.com/charts/view/artist-global-weekly/2023-04-13") # Diretcly calls from spotify.com, but is encrypted so using requests is harder that using a static html.
    print (top200)

    # makes an api call for each of the top 200 artists and stores the data as a list of tuples
    info = calc_artists_tuples(top200)
    
    # creates and populates a database with all the data
    cur, conn = db_setup("spotify_data")
    db_add_data(cur, conn, info)

    # print statement to confirm code ran (the api calls take a couple minutes)
    print("DONE RUNNING")