import os
from dotenv import load_dotenv
load_dotenv()

oai_auth = os.getenv('openAI_key')

print(oai_auth)