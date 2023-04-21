# library imports used in our functions
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
from bs4 import BeautifulSoup
import os
import sqlite3
import requests

# access name & key for the spotify API
cid = 'd590ddaa48094bbe9c51b98dff7dce8f'
secret = 'f72f507876014182a21b26571e60e31e'

# test conditions for calc_artists, top10pop, & top10len
birdy = ("Birdy",'spotify:artist:2WX2uTcsvV5OnS0inACecP')
boniver = ("Bon Iver", 'spotify:artist:4LEiUm1SRbFMgfqnQTwUbQ')
kanye = ("Ye",'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x')
jacklarsen = ("Jack Larsen", 'spotify:artist:1UGH6A3IionoSVLLmqtl4o')
bella = ("Ressa", 'spotify:artist:1zwvQUzM8t7zxyKFch91nX')
selena = ("Selena Gomez", 'spotify:artist:0C8ZW7ezQVs4URX5aX7Kqx')
artist_list = (birdy, boniver, kanye, jacklarsen, bella, selena)

        
# creates list of tuples for the top 200 artsists on spotify in the US (artist name, spotify URI)
def top200artists(html_file):

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
                # print("ARTIST:", artist_name)
                # print("SPOTIFY URI:", full_code)
                artist_tuple = (artist_name, code)
                top_200_artists.append(artist_tuple)
        # print (top_200_artists)
        return top_200_artists
    
# pulls from the spotify api to get an artists top 10 songs by poplarity
# and returns the poplarity scores as a list
# requires the artists spotify UID as a parameter
def top10(art):
    # pulls api request from spotipy library using our key
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    results = spotify.artist_top_tracks(art)
    
    
    #parses through data to get popularity score of top 10 songs 
    pop_list = [track['popularity'] for track in results['tracks']]
    len_list = [(track['duration_ms'])//1000 for track in results['tracks']]

    # returns list of the scores of the 10 most popular songs
    return (pop_list, len_list)
    
# pulls from the spotify api to get an artists top 10 songs by poplarity
# and returns the length of these songs in seconds as a list
# requires the artists spotify UID as a parameter
def top10len(art):
    # pulls api request from spotipy library using our key
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    results = spotify.artist_top_tracks(art, country='US')
    
    #cleans data up 
    # data = results.json()
    
    #parses through data to get popularity score of top 10 songs 
    len_list = [(track['duration_ms'])//1000 for track in results['tracks']]
    
    # print ("LENGTHS", len_list)
    # print ("AVG SONG LENGTH", (sum(len_list)/len(len_list)))

    # returns list of the lengths of the 10 most popular songs
    return len_list

# creates a list of dictionaries, one for each artist with the artists name as the key
# and then a list and average of popularity scores and song lengths
def calc_artists(artists):
    outlist = []
    for artist in artists:
        tempdic = {}
        pop_list = top10pop(artist[1])
        len_list = top10len(artist[1])
        print(pop_list)
        print(len_list)
        tempdic["Popularity Scores"] = pop_list
        tempdic["Average Popularity"] = sum(pop_list)/len(pop_list)
        tempdic["Length of Popular Songs"] = len_list
        tempdic["Average Length"] = sum(len_list)/len(len_list)

        artdic = {artist[0]:tempdic}
        outlist.append(artdic)
    return outlist

def main():
    top200 = top200artists("SPOTIFY APRIL 7-13.html")
    idlist = []
    finallist = []
    for artist in top200:
        idlist.append(artist[1])

    taylor = top10("06HL4z0CvFAxyc27GXpf02")
    print(taylor)
    # for id in idlist[:5]:
    #     final = top10(id)
    #     finallist.append(final)
    # print(finallist)
    
    # print(idlist)

    # top10(top200[1])

if __name__ == '__main__':
    main()

