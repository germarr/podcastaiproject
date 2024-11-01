from pydub import AudioSegment
import whisper


def audio_to_test(audioPath:str=None, textTitle:str=None, outputTranscript:str=None, lang:str='en'):
    # Load the Whisper model (you can also try "medium" or "large" models for more accuracy)
    model = whisper.load_model("base")

    # Transcribe the audio, specifying the language as Spanish ("es")
    result = model.transcribe(audioPath, language=lang)

    # Get the transcription text
    transcription = result['text']

    # Define the output file path (you can modify this to your desired path)
    if outputTranscript == None:
        output_file_path = f"../transcript/{textTitle}.txt"
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

# audio_to_test(audioPath=vid_title, textTitle=text_title)
# convert_mp3_to_wav(mp3_file = vid_title, wav_file = path_to_audio)