import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
import tiktoken
from openai import AzureOpenAI

transcript_with_time = pd.DataFrame([{
'start': segment['start'],  
    'end': segment['end'] ,    
    'text': segment['text'] 
} for segment in result['segments']])


# s is input text
def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.strip()
    
    return s

transcript_with_time['text']= transcript_with_time["text"].apply(lambda x : normalize_text(x))

tokenizer = tiktoken.get_encoding("cl100k_base")
transcript_with_time['n_tokens'] = transcript_with_time["text"].apply(lambda x: len(tokenizer.encode(x)))
transcript_with_time = transcript_with_time[transcript_with_time.n_tokens<8192]

# Create an empty list to store the chunks
chunks = []
current_chunk = []

# Initialize the progressive sum counter
current_sum = 0

for idx, row in transcript_with_time.iterrows():
    current_chunk.append(row)
    current_sum = row['progressive_sum']
    
    if current_sum >= 1400 or idx == len(transcript_with_time) - 1:
        # Convert the current_chunk list into a DataFrame and add it to the chunks list
        chunk_df = pd.DataFrame(current_chunk)
        chunks.append(chunk_df)
        
        # Reset the current chunk and the current sum
        current_chunk = []
        current_sum = 0

# If there's anything left in current_chunk, append it to chunks as well
if current_chunk:
    chunk_df = pd.DataFrame(current_chunk)
    chunks.append(chunk_df)

len(chunks)

# Initialize variables to track the cumulative sum and reset point
cumulative_sum = 0
new_col = []

# Iterate over the n_tokens column
for token in transcript_with_time['n_tokens']:
    # Add the current token to the cumulative sum
    cumulative_sum += token
    
    # If the cumulative sum exceeds 1400, reset to the current token value
    if cumulative_sum > 1400:
        cumulative_sum = token  # Reset the cumulative sum starting from the current token
        
    # Append the current cumulative sum to the new column list
    new_col.append(cumulative_sum)

# Create the new column in the DataFrame
transcript_with_time['progressive_sum'] = new_col

transcript_with_time.to_csv('./goop.csv')

import json
# Initialize variables
blobs = []
current_blob = {"start": None, "end": None, "text": ""}
cumulative_text = ""

# Iterate through the DataFrame rows
for index, row in transcript_with_time.iterrows():
    # If we're starting a new blob, record the 'start' time of the first row
    if current_blob["start"] is None:
        current_blob["start"] = row["start"]
    
    # Add the text to the current blob's text
    cumulative_text += " " + row["text"]
    
    # Update the 'end' time of the current blob to the current row's end time
    current_blob["end"] = row["end"]
    
    # If the 'progressive_sum' reaches or exceeds 1400, finalize this blob
    if row['progressive_sum'] >= 1400:
        current_blob['text'] = cumulative_text.strip()  # Strip leading spaces
        
        # Add the current blob to the list of blobs
        blobs.append(current_blob.copy())
        
        # Reset for the next blob
        current_blob = {"start": None, "end": None, "text": ""}
        cumulative_text = ""

# If there is any remaining text (in case the last chunk does not exceed 1400)
if cumulative_text:
    current_blob['text'] = cumulative_text.strip()
    blobs.append(current_blob.copy())

# Convert blobs to JSON format
result = json.dumps(blobs, indent=4)