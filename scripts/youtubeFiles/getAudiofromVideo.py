import re
import os
import yt_dlp
from videoTitle import getTitle
import argparse
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.audioToWav import audio_to_test, convert_mp3_to_wav
from scripts.embeddingsToDB import transcriptToTokens


# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Parse the arguments
args = parser.parse_args().input

urlOfTheVideo = args

def clean_filename(file_name: str, max_length: int = 255) -> str:
    # Replace any invalid character with an underscore
    cleaned_name = re.sub(r'[<>:"/\\|?*,.]', '', file_name)
    
    # Remove leading/trailing whitespace
    cleaned_name = cleaned_name.strip()
    
    # Replace multiple spaces or underscores with a single underscore
    cleaned_name = re.sub(r'[\s_]+', '_', cleaned_name)
    
    # Remove characters that are not letters or numbers
    cleaned_name = re.sub(r'[^a-zA-Z0-9_]', '', cleaned_name)
    
    # Trim to the maximum allowable length, if necessary
    cleaned_name = cleaned_name[:max_length]
    
    return cleaned_name.lower()

def create_folder(channelData: str = None):
    if not channelData:
        print("Invalid data: 'channel' key is required.")
        return

    # Define base directories
    base_dirs = ['../../audio', '../../wavAudio', '../../transcript', '../../answers']

    # Loop through base directories and create the channel path if it doesn't exist
    for base_dir in base_dirs:
        channel_path = os.path.join(base_dir, channelData)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)

    print(f"Folder '{channelData}' created successfully.")

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
    youtubeDictionary = getTitle(vTitle=ytbURL)

    channelName =  clean_filename(file_name=youtubeDictionary['channel'])
    videoTitle =  clean_filename(file_name=youtubeDictionary['title'])

    create_folder(channelData = channelName)
    download_video(videoURL=ytbURL, vTitle=videoTitle, vFolder=channelName)
    
    baseaudioURL = f"{channelName}/{videoTitle}"
    path_to_audio_mp3 = f"../../audio/{baseaudioURL}.mp3"
    path_to_audio_wav = f"../../wavAudio/{baseaudioURL}.wav"
    path_to_audio_transcript = f"../../transcript/{baseaudioURL}.txt"
    path_to_answers = f"../../answers/{baseaudioURL}.csv"
    
    convert_mp3_to_wav(mp3_file=path_to_audio_mp3, wav_file=path_to_audio_wav)
    audio_to_test(audioPath=path_to_audio_mp3, textTitle=videoTitle, outputTranscript=path_to_audio_transcript )

    ### INSERT SCRIPT TO CALCULATE THE TOTAL PRICE OF ADDING EMBEDDINGS INTO THE DB
    transcriptToTokens(transcript_path=path_to_audio_transcript, pathToCSV=path_to_answers)

    return path_to_audio_wav


if __name__ == "__main__":
    getRecordingFromYoutubeChannel(ytbURL = urlOfTheVideo)