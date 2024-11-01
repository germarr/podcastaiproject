import re
import os
from pydub import AudioSegment
import whisper
import pandas as pd

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

def create_folder(channelData: str = None, listOfFolders = None):
    if not channelData:
        print("Invalid data: 'channel' key is required.")
        return

    # Define base directories
    base_dirs = listOfFolders

    # Loop through base directories and create the channel path if it doesn't exist
    for base_dir in base_dirs:
        channel_path = os.path.join(base_dir, channelData)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)

    print(f"Folder '{channelData}' created successfully.")

def audio_to_text(audioPath:str=None, textTitle:str=None, outputTranscript:str=None, lang:str='en'):
    # Load the Whisper model (you can also try "medium" or "large" models for more accuracy)
    model = whisper.load_model("base")

    # Transcribe the audio, specifying the language as Spanish ("es")
    result = model.transcribe(audioPath, language=lang)

    # Get the transcription text
    transcription = result['text']

    # Define the output file path (you can modify this to your desired path)
    if outputTranscript == None:
        output_file_path = f"./transcript/{textTitle}.txt"
    else:
        output_file_path = f"{outputTranscript}"

    # Open the file in write mode and save the transcription
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(transcription)

    print(f"Transcription saved to {output_file_path}")
    return transcription

def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

def sendQToDb(ans_dict=None, file_path=None):
        
        answerDF = pd.DataFrame([ans_dict])
        
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        
        # Open the file in append mode
        with open(file_path, "a", encoding="utf-8") as file:
            if not file_exists:
                # If the file doesn't exist, write the headers and the first row
                answerDF.to_csv(file, index=False, header=True, lineterminator='\n')
            else:
                # If the file exists, only append the row without headers
                answerDF.to_csv(file, index=False, header=False, lineterminator='\n')

# audio_to_test(audioPath=vid_title, textTitle=text_title)
# convert_mp3_to_wav(mp3_file = vid_title, wav_file = path_to_audio)
