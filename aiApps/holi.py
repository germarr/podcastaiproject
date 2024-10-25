import os
from dotenv import load_dotenv
# load_dotenv()

# oai_auth = os.getenv('openAI_key')

# print(oai_auth)


import argparse


# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Parse the arguments
args = parser.parse_args().input

the_daily_rss = args #'https://feeds.megaphone.fm/profgmarkets'

print(the_daily_rss)