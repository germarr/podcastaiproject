import re
import os
import pandas as pd
from openai import AzureOpenAI
import tiktoken

### Langchanin Specific Libraries
from langchain_openai import AzureChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

import os
from dotenv import load_dotenv
load_dotenv()

oai_auth = os.getenv('openAI_key')
oai_endpoint = os.getenv('openAI_endpoint')
openAI_key_embeddings = os.getenv('openAI_key_embeddings')
openAI_endpoint_embeddings = os.getenv('openAI_endpoint_embeddings')
transcriptExample = os.getenv('transcriptExample')
answersExample = os.getenv('answersExample')
summaryExample = os.getenv('summaryExample')
questionsExample = os.getenv('questionsExample')

client = AzureOpenAI(
  api_key = openAI_key_embeddings,  
  api_version = "2023-05-15",
  azure_deployment='text-embedding-ada-002',
  azure_endpoint = openAI_endpoint_embeddings
)

llm = AzureChatOpenAI(
    azure_endpoint=oai_endpoint,
    openai_api_key = oai_auth,
    azure_deployment='gpt-35-turbo',
    openai_api_version="2024-05-01-preview",
)


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

def transcriptToTokens(transcript_path:str=None, pathToCSV:str=None):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)

    cook = TextLoader(transcript_path, encoding = 'UTF-8').load()
    text = text_splitter.split_documents(cook)

    df_bills = pd.DataFrame({'text':[i.page_content for i in text]})
    df_bills['text']= df_bills["text"].apply(lambda x : normalize_text(x))
    tokenizer = tiktoken.get_encoding("cl100k_base")
    df_bills['n_tokens'] = df_bills["text"].apply(lambda x: len(tokenizer.encode(x)))
    df_bills = df_bills[df_bills.n_tokens<8192]
    df_bills['ada_v2'] = df_bills["text"].apply(lambda x : generate_embeddings (x, model = 'text-embedding-ada-002')) # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model

    df_bills.to_csv(pathToCSV)

    return df_bills

prompts_for_summary = {
    "en":{
        "pro": """
            Please provide a comprehensive summary of the following text.
                  TEXT: {text}
                  SUMMARY:
                  """,
        "refine_pro":"""
                Write an expansive summary of the following text delimited by triple backquotes.
                Be detailed and be sure to cover the key points of the text.
                ```{text}```
                SUMMARY:
                """
    },
    "es":{
        "pro": """
            Escribe un resumen comprensivo del siguiente texto.
                  TEXTO: {text}
                  RESUMEN:
                  """,
        "refine_pro":"""
                Escribe un resumen expansivo del siguiente texto delimitado por comillas triples. 
                Sé detallado y asegúrate de cubrir los puntos clave del texto.
                ```{text}```
                RESUMEN:
                """
    }
}

def refine_summary(transcript_path:str=None, prompt_:str=None, refine_prompt_:str=None):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)

    cook = TextLoader(transcript_path, encoding = 'UTF-8').load()
    text = text_splitter.split_documents(cook)

    prompt = prompt_

    question_prompt = PromptTemplate(
        template=prompt, input_variables=["text"]
    )

    refine_prompt_template = refine_prompt_

    refine_template = PromptTemplate(
        template=refine_prompt_template, input_variables=["text"])

    # # Load refine chain
    # chain = load_summarize_chain(
    #     llm=llm,
    #     chain_type="refine", #refine
    #     question_prompt=question_prompt,
    #     refine_prompt=refine_template,
    #     return_intermediate_steps=True,
    #     input_key="input_documents",
    #     output_key="output_text",
    # )

    # Load refine chain
    chain = load_summarize_chain(
        llm=llm,
        chain_type="refine", #refine
        question_prompt=question_prompt,
        refine_prompt=refine_template,
        return_intermediate_steps=True,
        input_key="input_documents",
        output_key="output_text",
        verbose=True
    )

    result_summary = chain({"input_documents": text}, return_only_outputs=False)
    answer = result_summary['output_text']

    # Open the file in write mode and save the transcription
    # with open(summary_path, "w", encoding="utf-8") as file:
    #     file.write(answer)

    return answer, result_summary


