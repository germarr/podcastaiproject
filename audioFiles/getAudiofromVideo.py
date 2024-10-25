import re
import os
import yt_dlp
from pytube import YouTube

urlOfTheVideo = 'https://www.youtube.com/watch?v=fRs0OqV4uSc'

def clean_filename(file_name: str, max_length: int = 255) -> str:
    # Replace any invalid character with an underscore
    cleaned_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
    
    # Remove leading/trailing whitespace
    cleaned_name = cleaned_name.strip()
    
    # Replace multiple spaces or underscores with a single underscore
    cleaned_name = re.sub(r'[\s_]+', '_', cleaned_name)
    
    # Trim to the maximum allowable length, if necessary
    cleaned_name = cleaned_name[:max_length]
    
    return cleaned_name

def download_video(videoURL:str=None):
    yt = YouTube(videoURL)
    vid_title = clean_filename(file_name = yt.title.lower())

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }],
        'outtmpl': os.path.join('./audio', f'{vid_title}.%(ext)s'),
        'ffmpeg_location':"C:/Users/Ger M/Music/ffmpeg/bin"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])

        # ydl.download([theURL])

    return os.path.join('./audio', f'{vid_title}.mp3'),vid_title

vid_title,text_title = download_video(videoURL=urlOfTheVideo)

path_to_audio = f"../audio/{text_title}.wav"