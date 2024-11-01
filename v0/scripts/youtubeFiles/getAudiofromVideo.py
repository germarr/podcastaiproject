import re
import os
import yt_dlp
import argparse
import sys
from tabulate import tabulate

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Add the --type argument
# parser.add_argument('--isyoutube', type=str, required=True, help="The type of processing to apply")

# Parse the arguments
args = parser.parse_args()

# Access the input and type arguments
urlOfTheVideo = args.input
# processing_type = args.isyoutube

from videoTitle import channelStats,get_video_stats
from globalScripts import clean_filename, create_folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.audioToWav import audio_to_test, convert_mp3_to_wav
from scripts.embeddingsToDB import transcriptToTokens
from scripts.transcriptToEmbeddings import refine_summary
from embeddingDB.scripts.testingDBs import createSummaryDB,createAssetDB,createTranscriptDB,createEmbeddingDB,EmbeddingTranscript,df_to_sqlmodel,delete_channel_entries
from scripts.qanda import sendQToDb
import json
import pandas as pd



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

    youtubeDictionary, video_id,export_df = channelStats(youtubeURL=ytbURL, pathToSaveCSV='./videoStats/')

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
    
    language_ = 'es'
    
    if language_ == "en":
        transcriptstring = audio_to_test(audioPath=path_to_audio_mp3, textTitle=videoTitle, outputTranscript=path_to_audio_transcript,lang='en' )
        pro = """
            Please provide a comprehensive summary of the following text.
                  TEXT: {text}
                  SUMMARY:
                  """
        refine_pro_ = """
                Write an expansive summary of the following text delimited by triple backquotes.
                Be detailed and be sure to cover the key points of the text.
                ```{text}```
                SUMMARY:
                """
    else:
        transcriptstring = audio_to_test(audioPath=path_to_audio_mp3, textTitle=videoTitle, outputTranscript=path_to_audio_transcript,lang='es' )
        pro = """
            Escribe un resumen comprensivo del siguiente texto.
                  TEXTO: {text}
                  RESUMEN:
                  """
    
        refine_pro_ = """
                Escribe un resumen expansivo del siguiente texto delimitado por comillas triples. 
                Sé detallado y asegúrate de cubrir los puntos clave del texto.
                ```{text}```
                RESUMEN:
                """

    ### INSERT SCRIPT TO CALCULATE THE TOTAL PRICE OF ADDING EMBEDDINGS INTO THE DB
    df_bills = transcriptToTokens(transcript_path=path_to_audio_transcript, pathToCSV=path_to_answers)

    answer_summary, result_summary = refine_summary(transcript_path=path_to_audio_transcript,prompt_=pro, refine_prompt_=refine_pro_)

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

    createAssetDB(video_id,"youtube",videoTitle,channelName)
    createTranscriptDB(id_of_asset=video_id, transcriptSTR=transcriptstring)
    createSummaryDB(id_of_asset=video_id, transcriptsummary=answer_summary)
    
    df_gg  = pd.read_csv(path_to_answers,index_col=0)
    createEmbeddingDB(df_ = df_gg, class_info=EmbeddingTranscript, id_of_asset=video_id)

    is_video_in_last_fifty = export_df.query(f"video_id == '{video_id}'")['video_id'].count()
    
    print("👍 is video in last fifty | ", is_video_in_last_fifty, end=" | ")
    
    delete_channel_entries(channel_id_to_check = youtubeDictionary['channelid'])

    if is_video_in_last_fifty == 0:
        single_video_stats = get_video_stats(video_ids = video_id)
        single_df = pd.DataFrame(single_video_stats)
        print("HIGHER THAN 0 👌", end=" | ")
        # print(tabulate(single_df, headers='keys', tablefmt='pretty'))
        
        df_to_sqlmodel(df=single_df)
    
    print("LET'S PRINT EXPORT DF👌", end=" | ")
    # print(tabulate(export_df, headers='keys', tablefmt='pretty'))
    
    df_to_sqlmodel(df=export_df)

    
if __name__ == "__main__":
    getRecordingFromYoutubeChannel(ytbURL = urlOfTheVideo)