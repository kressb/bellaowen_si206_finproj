import urllib
import requests
import json
import sqlite3
from bs4 import BeautifulSoup
import os


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

        # loops through the artists on the top 200 weekly 
        # (from a static html page april 7-13 to avoid violating spotify's no scraping policy) 
        # and pulls their names and spotify URI
        # it then adds the spotify UID prefix to each and makes each artist a tuple (artist name, artist spotify URI)
        # it then returns this as a list of 200 artist tuples 
        for artist in artist_names:
                artist_name = artist.get_text(strip=True)
                top_200_artists.append(artist_name)

        return top_200_artists
    
def get_seatgeek_pop_score(artist):

    CLIENT_ID = 'MzMxNDQzNDF8MTY4MTc5ODQ1MC4zNTIwNjkx'
    SECRET = '31c2ebe5d78db857844d6e8c6e70c024ac29d90239cf5a2a67733de0f802374e'

    # connect
    


    # set api
    url = "https://api.seatgeek.com/2/performers"

    # set the parameters for the API request, including your API ID and secret
    params = {
        "q": artist,  # The performer you want to search for
        "client_id": CLIENT_ID,
        "client_secret": SECRET
    }

    # Send the API request and get the response
    response = requests.get(url, params=params)

    # check if request successful
    if response.status_code == 200:
        # get response data in JSON
        data = response.json()

        # extract performer data
        performer_data = data["performers"]
        performer_data = data["performers"][0]

        # return tuple of performer name and score
        return (performer_data["name"], performer_data["score"])
        # insert data into table




    conn.close()


if __name__ == '__main__':
    conn = sqlite3.connect('seatgeek.db')

    # c to access database & make changes
    c = conn.cursor()

    # create table
    c.execute('''CREATE TABLE seatgeek(artist TEXT, popularity score INT)''')
    final_list = []
    top200 = top200artists("SPOTIFY APRIL 7-13.html")
    for artist in top200[:100]:
        pop_score = get_seatgeek_pop_score(artist)
        c.execute('''INSERT INTO seatgeek VALUES(?,?)''', (pop_score[0], pop_score[1]))

        # commit data
        conn.commit()

        final_list.append(pop_score)
    print(final_list)

         