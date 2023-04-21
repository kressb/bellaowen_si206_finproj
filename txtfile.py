import sqlite3


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


artist_counts_to_txt('artist_count.txt')