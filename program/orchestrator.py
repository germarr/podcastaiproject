import argparse
import sys
import os

from youtube.downloadYoutubeVideo import download_video
from youtube.channelInformation_short import channelStats
from globalScripts import clean_filename, create_folder, convert_mp3_to_wav, audio_to_text,sendQToDb
from aiGlobalScripts import transcriptToTokens, refine_summary, prompts_for_summary
from database.dbconnectors import createAssetDB

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Add the --type argument
parser.add_argument('--isyoutube', type=str, required=True, help="The type of processing to apply")

# Add the --language argument
parser.add_argument('--language', type=str, required=True, help="The language for the process")


# Parse the arguments
args = parser.parse_args()

# Access the input and type arguments
urlOfTheVideo = args.input
isyoutube = args.isyoutube
language = args.language

if isyoutube == 'youtube':

    ### Step 1: Using the URL from a youtube video, get all the information from the channel, the video itself and the last 50 videos of the channel.
    #### For reference youtubeDictionary = {"channelid":channel_id, "title":video_title,"channelName":channel_name} 
    youtubeDictionary, video_id, dataframe_last50_videos = channelStats(youtubeURL=urlOfTheVideo, pathToSaveCSV='./videoStats/')

    ### Step 2: Get the Name of the Channel in a 'file friendly' format.
    channelName =  youtubeDictionary['channelName']
    videoTitle =  youtubeDictionary['title']
    channelID = youtubeDictionary['channelid']
    
    channelName_clean = clean_filename(file_name=channelName)
    videoTitle_clean = clean_filename(file_name=videoTitle)

    ### Step 3: Set up of the folders where the data is going
    create_folder(channelData = channelName_clean, listOfFolders=['./audio', './wavAudio', './transcript', './answers', './summary'])
    
    baseaudioURL = f"{channelName_clean}/{videoTitle_clean}"
    path_to_audio_mp3 = f"./audio/{baseaudioURL}.mp3"
    path_to_audio_wav = f"./wavAudio/{baseaudioURL}.wav"
    path_to_audio_transcript = f"./transcript/{baseaudioURL}.txt"
    path_to_answers = f"./answers/{baseaudioURL}.csv"
    path_to_summary = f"./summary/{baseaudioURL}"

    ### Step 4: Download the Video and turn it into an mp3 file.
    download_video(whereisaudiopath='./audio',videoid_=video_id, vTitle=videoTitle_clean, vFolder=channelName_clean)

    ### Step 5: Turn the mp3 file into a WAV file so it can be parsed with Whisper.
    convert_mp3_to_wav(mp3_file=path_to_audio_mp3, wav_file=path_to_audio_wav)

     ### Step 6: Crete the transcript of the video and store it in the respective folder.
    transcript_string = audio_to_text(audioPath=path_to_audio_mp3, textTitle=videoTitle_clean, outputTranscript=path_to_audio_transcript,lang=language)

    ### Step 7: Create a summary of the transcript.
    prompt_base = prompts_for_summary[language]['pro']
    prompt_refine = prompts_for_summary[language]['refine_pro']
    answer_summary, result_summary = refine_summary(transcript_path=path_to_audio_transcript,prompt_=prompt_base, refine_prompt_=prompt_refine)

    ### Step 8: Create a dataframe that stores the parsed transcript and the Embeddings for each chunk of text.
    embeddings_df = transcriptToTokens(transcript_path=path_to_audio_transcript, pathToCSV=path_to_answers)
    
    answerAndSummary = {
        "videoId":video_id,
        "summary":answer_summary
    }

    sendQToDb(ans_dict=answerAndSummary, file_path=f"{path_to_summary}.txt")

    ### Step 9: Send all the information to Postgres
    createAssetDB(channelID,channelName_clean,videoTitle_clean,video_id,isyoutube,videoTitle,channelName)










