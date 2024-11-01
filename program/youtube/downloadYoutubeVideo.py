import os
import yt_dlp


def download_video(whereisaudiopath:str=None,videoid_:str=None, vTitle:str=None, vFolder:str=None):

    pathOfAudio = f"{vFolder}/{vTitle}"

    videoURL = f"https://www.youtube.com/watch?v={videoid_}"

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }],
        'outtmpl': os.path.join(whereisaudiopath, f'{pathOfAudio}.%(ext)s'),
        'ffmpeg_location':"C:/Users/Ger M/Music/ffmpeg/bin"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])

        # ydl.download([theURL])

    return os.path.join(whereisaudiopath, f'{pathOfAudio}.mp3')