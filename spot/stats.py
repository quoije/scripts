from pymongo import MongoClient
from collections import Counter
from datetime import datetime
import requests

client = MongoClient('MANGODBSRV')
db = client['cluster0']
collection = db['spotify']

# Retrieve all the song documents from the collection
songs = collection.find()

# Initialize counters for song counts per month
song_counts = {}

# Group songs by month and calculate statistics for each month
for song in songs:
    song_name = song['song_name']  # Replace 'name' with the correct field name for song name
    artist_name = song['artist']  # Replace 'artist' with the correct field name for artist name
    song_id = song['song_id']  # Replace 'song_id' with the correct field name for the song ID
    play_date = song['date']  # Replace 'date' with the correct field name for the date
    
    # Parse the play date as a datetime object
    play_date = datetime.strptime(play_date, "%B %d, %Y at %I:%M%p")
    
    # Extract the month and year from the play date
    month = play_date.strftime("%B %Y")
    
    # Initialize the counter for the month if not already present
    if month not in song_counts:
        song_counts[month] = Counter()
    
    # Increment the song count for the month
    song_counts[month][(song_name, artist_name, song_id)] += 1

# Calculate the total plays for each month
total_plays = {month: sum(songs.values()) for month, songs in song_counts.items()}

# Spotify API endpoint for retrieving track information
endpointArtists = 'https://api.spotify.com/v1/artists'
endpointTracks = 'https://api.spotify.com/v1/tracks'

# Spotify API access token
access_token = 'ACCESSTOKENSPOTIFY'  # Replace with your actual access token

# Function to retrieve the genre for a given song ID
def get_song_info(song_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"{endpointTracks}/{song_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if 'artists' in data and data['artists']:
        artist = data['artists'][0]
        artist_id = artist['id']
        
        if 'genres' in artist and artist['genres']:
            genre = artist['genres'][0]
        else:
            genre = 'Unknown Genre'
    else:
        artist_id = 'Unknown Artist'
        genre = 'Unknown Genre'
        
    return genre, artist_id

# Function to retrieve the genre for a given song ID
def get_song_genre(artist_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"{endpointArtists}/{artist_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'genres' in data and data['genres']:
        genres = data['genres'][0]
        return genres
    return 'Unknown Genre'

# Print the statistics for each month
print("Song Statistics by Month:")
for month, songs in song_counts.items():
    print(f"Month: {month}")
    print(f"Total Plays: {total_plays[month]}")
    
    most_played_song = songs.most_common(1)[0]
    most_played_song_name = most_played_song[0][0]
    most_played_song_artist = most_played_song[0][1]
    most_played_song_id = most_played_song[0][2]
    
    genre = get_song_genre(get_song_info(most_played_song_id)[1])
    print(f"Most Played Song: {most_played_song_name} by {most_played_song_artist} ({most_played_song[1]} plays)")
    print(f"Most Played Song Genre: {genre}")
    
    print()  # Add a new line for better readability

# Calculate the total plays of all time
total_plays_all_time = sum(total_plays.values())

# Print the total plays of all time
print(f"Total Plays of All Time: {total_plays_all_time}")

# Close the MongoDB connection
client.close()