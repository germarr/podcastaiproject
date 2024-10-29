from googleapiclient.discovery import build
import re
import pandas as pd
from globalScripts import clean_filename, create_folder

import os
from dotenv import load_dotenv
load_dotenv()

youtube_key = os.getenv('youtube_key')
youtube = build('youtube', 'v3', developerKey=youtube_key)
urlOfVideo = 'https://www.youtube.com/watch?v=U7_oHUjRFjM'

def get_video_id(url):
    # Extract video ID from URL
    video_id = re.search(r"v=([^&]+)", url)
    if video_id:
        return video_id.group(1)
    return None

def getChannelId(videoid:str=None):
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=videoid
    )
    response = request.execute()
    if "items" in response and len(response["items"]) > 0:
        snippet = response["items"][0]["snippet"]
        channel_id = snippet["channelId"]
        video_title = snippet["title"]
        channel_name = snippet["channelTitle"]
        

    answer_dict = {"channelid":channel_id, "title":video_title,"channelName":channel_name}        

    return answer_dict

def get_uploads_playlist_id(api_key=youtube_key, chid:str=None):
    # Request channel details to get the uploads playlist ID
    request = youtube.channels().list(
        part="contentDetails,statistics",
        id=chid
    )
    response = request.execute()
    
    # Extract the uploads playlist ID
    base_dict = response['items'][0]
    uploads_playlist_id = base_dict['contentDetails']['relatedPlaylists']['uploads']
    stats = base_dict['statistics']

    channel_data = {
                "viewCount": stats['viewCount'],
                "subscriberCount": stats['subscriberCount'],
                "hiddenSubscriberCount": stats['hiddenSubscriberCount'],
                "videoCount": stats['videoCount'],
                "uploadId":uploads_playlist_id
        }

    return channel_data

def get_last_50_video_ids(playlist_id:str=None,api_key:str=youtube_key):
    video_ids = []
    next_page_token = None

    # Request to get videos in the uploads playlist, up to 50 videos
    request = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    # Extract video IDs
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_ids.append(video_id)

    return video_ids

def get_video_stats(video_ids):

    # Join video IDs into a single string
    video_ids_str = ','.join(video_ids)

    # Request to get video statistics for the last 50 videos
    request = youtube.videos().list(
        part="statistics,snippet,contentDetails",
        id=video_ids_str
    )

    response = request.execute()


    # Extract video stats
    video_stats = []
    
    for item in response['items']:
        individualVidData = item['snippet']
        globalVidData = item['id']
        individualVidDataStats = item['statistics']

        try:
            tagg = ",".join(individualVidData.get('tags'))
        except:
            tagg= "No Tags"

        video_stats.append({
        'video_id':globalVidData,
        'publishedAt':individualVidData['publishedAt'],
        'channelId':individualVidData['channelId'],
        'title':individualVidData['title'],
        'description':individualVidData['description'],
        'thumbnails':individualVidData['thumbnails']['default']['url'],
        'channelTitle':individualVidData['channelTitle'],
        'tags':tagg,
        'categoryId':individualVidData['categoryId'],
        'viewCount':individualVidDataStats.get('viewCount'),
        'likeCount':individualVidDataStats.get('likeCount'),
        'favoriteCount':individualVidDataStats.get('favoriteCount'),
        'commentCount':individualVidDataStats.get('commentCount')
    })

    return video_stats

def channelStats(youtubeURL:str=None, pathToSaveCSV:str=None):

    video_id = get_video_id(url=youtubeURL)
    channel_dict = getChannelId(video_id)
    video_title = clean_filename(file_name=channel_dict['title'])
    channel_data = get_uploads_playlist_id(chid = channel_dict['channelid'])
    upload_id = channel_data['uploadId']

    vids = get_last_50_video_ids(playlist_id=upload_id)
    vstats = get_video_stats(video_ids=vids)
    
    channel_name = clean_filename(file_name=channel_dict['channelName'])

    create_folder(channelData = channel_name, listOfFolders=[pathToSaveCSV])
    
    pd.DataFrame(vstats).to_csv(f"{pathToSaveCSV}/{channel_name}/{video_title}.csv")

    return channel_dict, video_id

if __name__ == "__main__":
    getChannelId(vTitle="https://www.youtube.com/watch?v=cW7Qrrkl9hE")