import urllib
import requests
import json
import sqlite3


apikey = 'PdDGWABexe2JEt0fSGVccMK4X1aIed3N'
secret = 'yPBiIbd4w5XphzFi'



url = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={apikey}&keyword=Taylor%20Swift&sort=date,asc&size=5&include=venues,ticketFeatures&locale=en-us&currency=USD'

response = requests.get(url)

conn = sqlite3.connect("taylor_events.db")
cursor = conn.cursor()

# Create the events table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS taylor_events (
        spotify_artist_id TEXT,
        artist_name TEXT,
        event_name TEXT,
        venue_name TEXT,
        date TEXT,
        city TEXT,
        state TEXT,
        price_min INT,
        price_max INT
    )
""")

artist_name = "Taylor Swift"

# Parse the JSON response and extract the event details
data = response.json()
events = data["_embedded"]["events"]
for event in events:
    name = event["name"]
    if "start" in event["dates"]:
        date = event["dates"]["start"]["localDate"]
    else:
        date = event["dates"]["access"]["startDateTime"]
    venue = event["_embedded"]["venues"][0]["name"]
    city = event["_embedded"]["venues"][0]["city"]["name"]
    state = event["_embedded"]["venues"][0]["state"]["name"]
    if "priceRanges" in event:
        price_min = event["priceRanges"][0]["min"]
        price_max = event["priceRanges"][0]["max"]
    else:
        price_min = "No min"
        price_max = "No max"
    artist_id = 1
    print(f"{name} - {city}, {state} - {venue} - {date} - ${price_min} to ${price_max}")
    cursor.execute("INSERT INTO taylor_events (spotify_artist_id, artist_name, event_name, venue_name, date, city, state, price_min, price_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (artist_id, artist_name, name, venue, date, city, state, price_min, price_max))
    conn.commit()


# Close the database connection
conn.close()