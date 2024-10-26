from langchain_openai import AzureChatOpenAI, AzureOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

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

import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

oai_auth = os.getenv('openAI_key')
oai_endpoint = os.getenv('openAI_endpoint')
openAI_key_embeddings = os.getenv('openAI_key_embeddings')
openAI_endpoint_embeddings = os.getenv('openAI_endpoint_embeddings')
transcriptExample = os.getenv('transcriptExample')
answersExample = os.getenv('answersExample')

llm = AzureChatOpenAI(
    azure_endpoint=oai_endpoint,
    openai_api_key = oai_auth,
    azure_deployment='gpt-35-turbo',
    openai_api_version="2024-05-01-preview",
)

client = AzureOpenAI(
  api_key = openAI_key_embeddings,  
  api_version = "2023-05-15",
  azure_deployment='text-embedding-ada-002',
  azure_endpoint = openAI_endpoint_embeddings
)

def refine_summary(transcript_path:str=None):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=10)

    cook = TextLoader(transcript_path, encoding = 'UTF-8').load()
    text = text_splitter.split_documents(cook)

    return text

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

def generate_embeddings(text, model="text-embedding-ada-002"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_docs(df, user_query, top_n=4, to_print=True):
    embedding = generate_embeddings(
        user_query,
        model="text-embedding-ada-002" # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )

    if to_print:
        print(res)

    return res

def refine_summary(transcript_path:str=None):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=10)

    cook = TextLoader(transcript_path, encoding = 'UTF-8').load()
    text = text_splitter.split_documents(cook)

    prompt = """
            Please provide a summary of the following text.
                  TEXT: {text}
                  SUMMARY:
                  """

    question_prompt = PromptTemplate(
        template=prompt, input_variables=["text"]
    )

    refine_prompt_template = """
                Write a concise summary of the following text delimited by triple backquotes.
                Return your response in bullet points which covers the key points of the text.
                IF IT SOUNDS LIKE AN ADVERTISMENT RETURN 'AD NO RELEVANT'
                ```{text}```
                BULLET POINT SUMMARY:
                """

    refine_template = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"])

    # Load refine chain
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_template,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text",
    )

    result_summary = chain({"input_documents": text}, return_only_outputs=False)
    answer = result_summary['output_text']

    # Open the file in write mode and save the transcription
    with open(transcript_path, "w", encoding="utf-8") as file:
        file.write(answer)

    return answer

def getTranscriptContent(transcriptp:str=None):

    ll = refine_summary(transcript_path=transcriptp)
    df_bills = pd.DataFrame({'text':[i.page_content for i in ll]})
    df_bills['text']= df_bills["text"].apply(lambda x : normalize_text(x))
    tokenizer = tiktoken.get_encoding("cl100k_base")
    df_bills['n_tokens'] = df_bills["text"].apply(lambda x: len(tokenizer.encode(x)))
    df_bills = df_bills[df_bills.n_tokens<8192]
    df_bills['ada_v2'] = df_bills["text"].apply(lambda x : generate_embeddings (x, model = 'text-embedding-ada-002')) # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model

    return df_bills

df_bills = getTranscriptContent(transcriptp=transcriptExample)

res = search_docs(df_bills, "What factors are the men considering for this election?", top_n=4)

allTEXTS = res['text'].to_list() 
single_string = " ".join(allTEXTS)

with open(answersExample, "w", encoding="utf-8") as file:
    file.write(single_string)

aah=refine_summary(transcript_path=answersExample)