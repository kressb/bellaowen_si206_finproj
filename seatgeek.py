import urllib
import requests
import json
import pandas as pd

CLIENT_ID = 'MzMxNDQzNDF8MTY4MTc5ODQ1MC4zNTIwNjkx'
SECRET = '31c2ebe5d78db857844d6e8c6e70c024ac29d90239cf5a2a67733de0f802374e'

# Set the API endpoint URL
url = "https://api.seatgeek.com/2/performers"

# Set the parameters for the API request, including your API ID and secret
params = {
    "q": "elton john",  # The performer you want to search for
    "client_id": CLIENT_ID,
    "client_secret": SECRET
}

# Send the API request and get the response
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Get the data from the response in JSON format
    data = response.json()

    # Extract the performer data
    performer_data = data["performers"]
    performer_data = data["performers"][0]

    # Print the performer score
    print("Performer Name: ", performer_data["name"])
    print("Performer Score: ", performer_data["score"])



