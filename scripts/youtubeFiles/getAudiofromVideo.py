import re
import os
import yt_dlp
from videoTitle import channelStats
from globalScripts import clean_filename, create_folder
import argparse
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.audioToWav import audio_to_test, convert_mp3_to_wav
from scripts.embeddingsToDB import transcriptToTokens
from scripts.transcriptToEmbeddings import refine_summary
from scripts.qanda import sendQToDb
import json

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Parse the arguments
args = parser.parse_args().input

urlOfTheVideo = args

def download_video(videoURL:str=None, vTitle:str=None, vFolder:str=None):

    pathOfAudio = f"{vFolder}/{vTitle}"

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }],
        'outtmpl': os.path.join('../../audio', f'{pathOfAudio}.%(ext)s'),
        'ffmpeg_location':"C:/Users/Ger M/Music/ffmpeg/bin"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoURL])

        # ydl.download([theURL])

    return os.path.join('../../audio', f'{pathOfAudio}.mp3')

def getRecordingFromYoutubeChannel(ytbURL:str=None):

    youtubeDictionary, video_id = channelStats(youtubeURL=ytbURL, pathToSaveCSV='./videoStats/')

    channelName =  clean_filename(file_name=youtubeDictionary['channelName'])
    videoTitle =  clean_filename(file_name=youtubeDictionary['title'])

    create_folder(channelData = channelName, listOfFolders=['../../audio', '../../wavAudio', '../../transcript', '../../answers', '../../summary'])
    download_video(videoURL=ytbURL, vTitle=videoTitle, vFolder=channelName)
    
    baseaudioURL = f"{channelName}/{videoTitle}"
    path_to_audio_mp3 = f"../../audio/{baseaudioURL}.mp3"
    path_to_audio_wav = f"../../wavAudio/{baseaudioURL}.wav"
    path_to_audio_transcript = f"../../transcript/{baseaudioURL}.txt"
    path_to_answers = f"../../answers/{baseaudioURL}.csv"
    path_to_summary = f"../../summary/{baseaudioURL}"
    
    convert_mp3_to_wav(mp3_file=path_to_audio_mp3, wav_file=path_to_audio_wav)
    audio_to_test(audioPath=path_to_audio_mp3, textTitle=videoTitle, outputTranscript=path_to_audio_transcript )

    ### INSERT SCRIPT TO CALCULATE THE TOTAL PRICE OF ADDING EMBEDDINGS INTO THE DB
    transcriptToTokens(transcript_path=path_to_audio_transcript, pathToCSV=path_to_answers)

    answer_summary, result_summary = refine_summary(transcript_path=path_to_audio_transcript)

    answerAndSummary = {
        "videoId":video_id,
        "summary":answer_summary
    }

    sendQToDb(ans_dict=answerAndSummary, file_path=f"{path_to_summary}.txt",)

    try:
        with open(f"{path_to_summary}_full.txt",'w',encoding='utf-8') as file:
            file.write(json.dumps(str(result_summary), indent=4))
    except:
        print(result_summary)


if __name__ == "__main__":
    getRecordingFromYoutubeChannel(ytbURL = urlOfTheVideo)