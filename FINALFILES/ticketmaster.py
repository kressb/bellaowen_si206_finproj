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
    
def get_event_prices(artist):

    apikey = 'PdDGWABexe2JEt0fSGVccMK4X1aIed3N'
    secret = 'yPBiIbd4w5XphzFi'


    url = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={apikey}&keyword={artist}&sort=date,asc&size=5&Features&locale=en-us&currency=USD'

    response = requests.get(url)

    # conn = sqlite3.connect("event_prices.db")
    # cursor = conn.cursor()

    # # create the events table if it does not exist
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS events (
    #         artist_name TEXT,
    #         event_1_price_range TEXT,
    #         event_2_price_range TEXT,
    #         event_3_price_range TEXT,
    #         event_4_price_range TEXT,
    #         event_5_price_range TEXT,
    #     )
    # """)

    # parse the JSON response and extract the event details
    data = response.json()
    print(data)
    events = data["_embedded"]["events"]
    max_list = []
    for event in events:
            # if "name" in event:
            #     name = event["name"]
            # else:
            #     name = "No name found"
            # if "start" in event["dates"]:
            #     date = event["dates"]["start"]["localDate"]
            # else:
            #     date = event["dates"]["access"]["startDateTime"]
            # venue = event["_embedded"]["venues"][0]["name"]
            # city = event["_embedded"]["venues"][0]["city"]["name"]
            # state = event["_embedded"]["venues"][0]["state"]["name"]
        if "priceRanges" in event:
            price_max = event["priceRanges"][0]["max"]
        else:
            price_max = "No max"
        range = price_max
        max_list.append(range)
        # cursor.execute("INSERT INTO events (artist_name, event_1_price_range, event_2_price_range, event_3_price_range, event_4_price_range, event_5_price_range) VALUES (?, ?, ?, ?, ?)", (price_min, price_max))
        # conn.commit()
    return max_list

get_event_prices('Future')

    # close the database connection
    # conn.close()
# def main():
    # dic = {}
    # top200 = top200artists("SPOTIFY APRIL 7-13.html")
    # for artist in top200[:9]:
    #     event_ranges = get_event_prices(artist)
    #     dic.update({artist: event_ranges})
    # print(dic)

# if __name__ == '__main__':
#     main()