from rssParser import getMP3URL
from getAudioFromMp3 import getAudioFromMp3
from audioToWav import audio_to_test, convert_mp3_to_wav
from audioDiarization import wav_to_diarization, diarization_to_csv
import argparse


# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Parse the arguments
args = parser.parse_args().input

the_daily_rss = args 
 
rss_feed = the_daily_rss

def main():
    mp3data = getMP3URL(mp3URL=rss_feed)
    print(mp3data)
    mp3_filename, episode = getAudioFromMp3(mp3URL = mp3data['rss_url'], episodeName = mp3data['episode_title'])

    audio_to_test(audioPath=mp3_filename, textTitle=episode)

    wav_episode_title = f"../wavAudio/{episode}.wav"

    convert_mp3_to_wav(mp3_file = mp3_filename, wav_file= wav_episode_title)

    diarization = wav_to_diarization(pipeline_path=wav_episode_title)
    speakers_df = diarization_to_csv(diar=diarization, pToAudio=wav_episode_title, episodeTitle=episode)

    print(speakers_df)


if __name__ == "__main__":
    main()