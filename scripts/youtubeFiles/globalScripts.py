import re
import os

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
