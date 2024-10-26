import requests
import os
import re

def sanitize_filename(input_string):
    """
    This function removes problematic characters from the input string,
    replaces spaces with underscores, and ensures the string is safe
    to be used as a filename.

    :param input_string: The original string to sanitize.
    :return: A sanitized string that is safe to use as a filename.
    """
    # Replace spaces with underscores
    sanitized_string = input_string.replace(' ', '_')

    # Remove any characters that are not alphanumeric, underscore, hyphen, or dot
    # This will remove characters like / \ : * ? " < > | from the filename
    sanitized_string = re.sub(r'[\/:*?"<>|]', '', sanitized_string)

    # Optionally, you could also remove any leading/trailing dots or spaces
    sanitized_string = sanitized_string.strip('.')

    return sanitized_string.lower()

def getAudioFromMp3(mp3URL:str=None, episodeName:str=None):

    # URL of the MP3 file
    mp3_url = mp3URL

    # Title of the Audi
    episode= sanitize_filename(input_string = episodeName)

    # Directory where the MP3 will be saved
    directory = "../audio/"
    file_path = os.path.join(directory, f"{episode}.mp3")

    # Send a GET request to the MP3 URL
    response = requests.get(mp3_url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open a local file with write-binary mode
        with open(file_path, 'wb') as mp3_file:
            # Write the content in chunks to avoid high memory usage
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    mp3_file.write(chunk)
        print(f"MP3 downloaded successfully as '{episode}'")
    else:
        print(f"Failed to download MP3. Status code: {response.status_code}")

    return file_path , episode
