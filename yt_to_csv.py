import os
import requests
import csv
import time
import random

# Environment variable for your YouTube API key
# This key allows your program to interact with the YouTube API
YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
# YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"

# ID of the YouTube channel you're interested in (in this case, echohive is the channel)
CHANNEL_ID = "UCL7przoMtZTmiQMhc9ifIww"

# The base URL of the YouTube Data API
# All YouTube API requests begin with this URL
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3/"

def get_channel_videos(channel_id, num_videos=None):
    # Define the URL for the API request to get the channel's details
    url = f"{YOUTUBE_API_BASE_URL}channels?part=contentDetails&id={channel_id}&key={YOUTUBE_API_KEY}"
    
    # Send a GET request to the YouTube API
    response = requests.get(url)
    
    # Parse the response as JSON
    channel_data = response.json()
    
    # Extract the ID of the channel's 'uploads' playlist, which contains all its videos
    uploads_playlist_id = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Initialize a list to hold the details of each video
    videos = []
    
    # Initialize a variable to hold the token for the next page of results
    next_page_token = None
    
    # Initialize a counter for the number of videos retrieved
    video_count = 0

    # Use a loop to retrieve all videos in the 'uploads' playlist
    while True:
        # Define the URL for the API request to get the playlist's videos
        url = f"{YOUTUBE_API_BASE_URL}playlistItems?part=snippet&maxResults=50&playlistId={uploads_playlist_id}&key={YOUTUBE_API_KEY}"
        
        # If there's a next page token, add it to the URL
        if next_page_token:
            url += f"&pageToken={next_page_token}"
        
        # Send a GET request to the YouTube API
        response = requests.get(url)
        
        # Parse the response as JSON
        playlist_data = response.json()
        
        # Add the details of each video to the list
        videos.extend(playlist_data['items'])

        # Update the count of videos retrieved
        video_count += len(playlist_data['items'])

        # If we've retrieved enough videos, break the loop
        if num_videos and video_count >= num_videos:
            videos = videos[:num_videos]
            break

        # Get the token for the next page of results
        next_page_token = playlist_data.get('nextPageToken')
        
        # If there's no next page token, break the loop
        if not next_page_token:
            break

    # Return the list of videos
    return videos

def save_videos_to_csv(videos, file_name, append=False):
    # If we're appending...
    if append:
        # Read the existing data
        with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            existing_data = list(reader)
    
    # Open the CSV file for writing
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(["video_id", "title", "description", "url"])
        
        # If we're appending, write the new data first
        if append:
            for video in videos:
                write_video_to_csv(video, csv_writer)

        # If we were appending, write the old data after the new data
        if append:
            # Skip the header row in the old data
            for row in existing_data[1:]:
                csv_writer.writerow(row)

        # If we're not appending, just write the new data
        if not append:
            for video in videos:
                write_video_to_csv(video, csv_writer)

def write_video_to_csv(video, csv_writer):
    # Extract video ID from the video details
    video_id = video['snippet']['resourceId']['videoId']
    
    # Extract title from the video details
    title = video['snippet']['title']
    
    # Extract description from the video details
    description = video['snippet']['description']
    
    # Construct the URL of the video
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Write the video's details to a row in the CSV file
    csv_writer.writerow([video_id, title, description, url])
    
    # Wait for a random amount of time to avoid overwhelming the server with requests
    # time.sleep(1 + 5 * random.random())
    
    # Print a message to show that the video's details have been saved
    print(f"Saved video {video_id} to CSV")


def main():
    # Ask the user for the number of latest videos to fetch
    num_videos = input("Enter the number of latest videos to fetch (or 'all' for all videos): ")
    
    # If the user entered 'all', set num_videos to None
    if num_videos.lower() == 'all':
        num_videos = None
    # Otherwise, convert num_videos to an integer
    else:
        num_videos = int(num_videos)

    # Ask the user whether they want to append the data to the existing CSV file
    append_choice = input("Do you want to append the data to the existing CSV file? (yes/no): ")

    # If the user entered 'yes', set append to True
    if append_choice.lower() == 'yes':
        append = True
    # Otherwise, set append to False
    else:
        append = False

    # Get the videos from the channel
    videos = get_channel_videos(CHANNEL_ID, num_videos)
    
    # Save the videos to the CSV file
    save_videos_to_csv(videos, 'videos.csv', append)

# If this script is being run directly (as opposed to being imported), call the main function
if __name__ == "__main__":
    main()
