import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your Spotify API credentials
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8888/callback'  # Provide a valid redirect URI

# Create an authorization flow object
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Get the authorization URL
auth_url = auth_manager.get_authorize_url()

# Print the authorization URL and follow it in your browser
print(f"Please visit this URL to authorize the application: {auth_url}")

# Once authorized, you will be redirected to the specified redirect URI, and the authorization code will be appended to the URL.
# Extract the authorization code from the redirected URL and provide it to the auth_manager to obtain the access token.
authorization_code = input("Enter the authorization code: ")
auth_manager.get_access_token(authorization_code)

# Retrieve the access token
access_token = auth_manager.get_access_token()['access_token']
print(f"Access Token: {access_token}")