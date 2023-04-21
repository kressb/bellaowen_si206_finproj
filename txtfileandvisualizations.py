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

def makeBarChart():
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

# artist_counts_to_txt('artist_count.txt')
makeScatterPlot()
makeBarChart()