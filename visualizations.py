import sqlite3
import matplotlib.pyplot as plt

def artist_counts_to_txt(file):

    # Connect to the SQLite database
    conn = sqlite3.connect('billboard_songs.db')
    cursor = conn.cursor()

    # Execute the SQL query to count the number of artists and select their names
    cursor.execute("SELECT artist_name, count FROM artist_counts ORDER BY count DESC")
    results = cursor.fetchall()

    # Write the results to a txt file
    with open(file, 'w') as f:
        for row in results:
            artist = row[0]
            count = row[1]
            f.write(f'{artist} has {count} song(s) in the billboard hot top 100\n')

    # Close the database connection
    conn.close()

# Artist Popularity vs number of top 100 songs
def makeScatterPlot():
    # Connect to the SQLite database
    conn = sqlite3.connect('spotify_data_correct.db')
    cursor1 = conn.cursor()

    conn2 = sqlite3.connect('billboard_songs.db')
    cursor2 = conn2.cursor()

    #  attach the second database to the first database connection
    cursor1.execute("ATTACH DATABASE 'billboard_songs.db' as db2")

    cursor = conn.cursor()

    # Execute the SQL query to join the spotify and artist_count tables
    cursor.execute("SELECT spotify_data.average_popularity, IFNULL(artist_counts.count, 0) FROM spotify_data LEFT JOIN db2.artist_counts ON spotify_data.artist_name = db2.artist_counts.artist_name")
    results = cursor.fetchall()

    # Extract the x and y values from the results
    y = [row[0] for row in results]
    x = [row[1] for row in results]

    # Create a scatter plot using matplotlib.pyplot
    plt.scatter(x, y)
    plt.ylabel('Popularity Score')
    plt.xlabel('Song Count')
    plt.title('Average Popularity vs. Number of Songs in Top 100')
    plt.show()

    # Close the database connection
    conn.close()

# Scatter plot of artist avg song length vs artist avg popularity 
def makeScatter2():
    conn = sqlite3.connect('spotify_data_correct.db')
    cursor = conn.cursor()

    cursor.execute("SELECT average_popularity, average_length FROM spotify_data")
    results = cursor.fetchall()

    # Extract the x and y values from the results
    x = [row[0] for row in results]
    y = [row[1] for row in results]

    # Create a scatter plot using matplotlib.pyplot
    plt.scatter(x, y)
    plt.xlabel('Popularity Score')
    plt.ylabel('Average Song Length')
    plt.title('Popularity Score vs. Song Lengths')

    # Show the plot
    plt.show()

    # Close the database connection
    conn.close()

# Bar chart of artist avg song length vs artist avg popularity 
def make_bar_chart():
    # Connect to the SQLite database
    conn = sqlite3.connect('spotify_data_correct.db')  
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT average_length, average_popularity FROM spotify_data") 
    rows = cursor.fetchall()

    # Extract categories and values from the fetched data
    categories = [row[0] for row in rows]
    values = [row[1] for row in rows]

    # Create the bar chart
    plt.bar(categories, values, color='blue', width=1)

    # Customize the chart
    plt.ylim(50, 100)
    plt.xlim(100, 300)
    plt.xlabel("Average Song Length (s)")
    plt.ylabel("Spotify Popularity Score")
    plt.title("Song Length vs Popularity Bar Chart")
    plt.show()  

    # Close the database connection
    conn.close()

# spotify vs seatgeek popularity scores for top 10 spotify artists
def make_grouped_bar_chart():
    # Connect to the first SQLite database (spotify_data_correct.db)
    conn1 = sqlite3.connect('spotify_data_correct.db')
    cursor1 = conn1.cursor()

    # Get top 10 artists from spotify
    cursor1.execute("SELECT artist_name, average_popularity FROM spotify_data ORDER BY spotify_rank ASC LIMIT 10")
    spotify_data = cursor1.fetchall()
    artists_spotify = [row[0] for row in spotify_data]
    popularity_scores_spotify = [row[1] for row in spotify_data]

    # get the seatgeek database and data
    conn2 = sqlite3.connect('seatgeek.db')
    cursor2 = conn2.cursor()
    seatgeek_data = []
    for artist in artists_spotify:
        cursor2.execute("SELECT popularity FROM seatgeek WHERE artist=?", (artist,))
        seatgeek_score = cursor2.fetchone()
        seatgeek_data.append(seatgeek_score[0]*100 if seatgeek_score else 0) 
    popularity_scores_seatgeek = seatgeek_data

    # chart setup
    width = 0.3  
    fig, ax1 = plt.subplots()  
    ax2 = ax1.twinx() 
    index = range(len(artists_spotify))

    # Plots the bars
    ax1.bar(index, popularity_scores_spotify, width, label='Spotify', color='blue')
    ax1.bar([i + width for i in index], popularity_scores_seatgeek, width, label='SeatGeek', color='orange')
    
    # Set labels, titles, and legend
    ax1.set_xlabel('Artists')
    ax1.set_ylabel('Spotify Popularity Score (0-100)')
    ax1.set_title('Spotify vs. SeatGeek Popularity Score Comparison (of the top 10 Spotify artists)')
    ax1.set_xticks([i + width / 2 for i in index])
    ax1.set_xticklabels(artists_spotify, rotation=30, ha='right')
    ax1.legend()
    ax2.set_ylabel('SeatGeek Popularity Score (0-1)')

    # Display or save the chart
    plt.show()  

    conn1.close()
    conn2.close()

# deecending bar chart of top 10 artists with the most songs on the billboard top 100
def plot_artist_songs_chart():
    # gets the info from the database
    conn = sqlite3.connect('billboard_songs.db')
    cur = conn.cursor()
    cur.execute("SELECT artist_name, SUM(count) as num_songs FROM artist_counts GROUP BY artist_name ORDER BY num_songs DESC LIMIT 10")
    data = cur.fetchall()
    artists = [row[0] for row in data]
    num_songs = [row[1] for row in data]

    # cretate the bars
    fig, ax = plt.subplots()
    index = range(len(artists))
    ax.bar(index, num_songs, color='blue')

    # plot the bars and axises and titles
    ax.set_xlabel('Artists (Top 10)')
    ax.set_ylabel('Number of Songs on the Billboard Top 100')
    ax.set_title('Artists with Most Songs on the Billboard Top 100')
    ax.set_xticks(index)
    ax.set_xticklabels(artists, rotation=30, ha='right')

    plt.show() 
   
    conn.close()
    cur.close()


# runs all of the visualizations
def main():
    artist_counts_to_txt('artist_count.txt')
    makeScatterPlot()
    makeScatter2()
    # make_bar_chart() # NO LONGER USING, REPETITIVE
    make_grouped_bar_chart()
    plot_artist_songs_chart()

main()
