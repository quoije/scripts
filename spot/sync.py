import os
import gspread
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pymongo import MongoClient

# Replace 'credentials.json' with the path to your downloaded credentials JSON file
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/drive'])

# Create a Drive API service client
drive_service = build('drive', 'v3', credentials=credentials)

def get_google_sheets_in_folder(folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'",
        fields='files(id, name)'
    ).execute()

    sheets = results.get('files', [])

    return sheets

# Replace 'folder_id' with the actual ID of the folder you want to retrieve sheets from
folder_id = '1TaG1w1UemFNFzOENX34TjHu-4YWkGRGw'

# Call the function to get the Google Sheets in the folder
sheets = get_google_sheets_in_folder(folder_id)

# Check if the credentials are expired and refresh them if necessary
if credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())

# Create a gspread client using the refreshed credentials
gc = gspread.authorize(credentials)

# Connect to your MongoDB server
client = MongoClient('MONGODBSRV')

# Replace 'mydatabase' and 'mycollection' with your actual database and collection names
db = client['cluster0']
collection = db['spotify']

# Loop through the sheets
for sheet in sheets:
    sheet_id = sheet['id']

    # Open the Google Sheet by its ID
    sheet = gc.open_by_key(sheet_id)

    # Access a specific worksheet (e.g., the first sheet)
    worksheet = sheet.get_worksheet(0)

    # Extract the data from the worksheet
    data = worksheet.get_all_values()

    # Convert the data into a list of dictionaries
    headers = data[0]
    rows = data[1:]
    rows_dict = []

    # Map the data to the desired field names
    field_names = ['date', 'song_name', 'artist', 'song_id', 'song_url']
    for row in rows:
        row_dict = {}
        for i, field_name in enumerate(field_names):
            row_dict[field_name] = row[i]
        rows_dict.append(row_dict)
        print("-----------------")
        print(row_dict)
        print("-----------------")

    # Insert the data into MongoDB
    collection.insert_many(rows_dict)

client.close()