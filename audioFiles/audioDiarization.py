import pandas as pd
import os
import shutil
import subprocess
from pyannote.audio import Pipeline
import whisper
from pyannote.audio.pipelines.utils.hook import ProgressHook

import os
from dotenv import load_dotenv
load_dotenv()

diraization_key = os.getenv('hugging_face_diarization')

# Load the Whisper model (you can also try "medium" or "large" models for more accuracy)
model = whisper.load_model("base")

def extract_audio_segment(input_file, start_time, end_time, output_file):
    # Use ffmpeg to extract the audio segment
    subprocess.run([
        "ffmpeg", "-i", input_file,
        "-ss", str(start_time), "-to", str(end_time),
        "-c", "copy", output_file
    ])

def delete_all_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # print(f"The folder {folder_path} does not exist.")
        return
    
    # Remove all files and subdirectories inside the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isfile(item_path):
            os.remove(item_path)
            # print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Delete subdirectory and its contents
            # print(f"Deleted directory: {item_path}")

    print(".",end="")

def wav_to_diarization(pipeline_path:str=None):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=diraization_key)

    with ProgressHook() as hook:
        # diarization = pipeline(pipeline_path, hook=hook, num_speakers=2)
        diarization = pipeline(pipeline_path, hook=hook)

    return diarization

def diarization_to_csv(diar=None, pToAudio:str=None, episodeTitle:str=None):

    #Function to extract an audio segment
    speaking_dict = []

    # Loop through speaker segments and transcribe each one
    for segment, _, speaker in diar.itertracks(yield_label=True):
        # Extract the segment of audio for this speaker
        segment_file = f"../segments/speaker_{speaker}_{segment.start:.1f}_to_{segment.end:.1f}.wav"
        extract_audio_segment(pToAudio, segment.start, segment.end, segment_file)

        # Run Whisper transcription on the segment
        transcription = model.transcribe(segment_file)
        
        speaking_dict.append({
            "speaker":speaker,
            "timestamp":f"start {segment.start:.1f}s - end {segment.end:.1f}s",
            "transcription":transcription['text']
        })

        delete_all_in_folder(folder_path='../segments')

    fileToExport = pd.DataFrame(speaking_dict)

    fileToExport.to_csv(f'../diarization/{episodeTitle}.csv')
    
    return fileToExport
