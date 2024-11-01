from langchain_openai import AzureChatOpenAI
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
from dotenv import load_dotenv
load_dotenv()

oai_auth = os.getenv('openAI_key')
oai_endpoint = os.getenv('openAI_endpoint')

llm = AzureChatOpenAI(
    azure_endpoint=oai_endpoint,
    openai_api_key = oai_auth,
    azure_deployment='gpt-35-turbo',
    openai_api_version="2024-05-01-preview",
)

folder_template = "../transcript/example.txt"

def refine_summary(transcript_path:str=None, prompt_:str="""
            Please provide a comprehensive summary of the following text.
                  TEXT: {text}
                  SUMMARY:
                  """, refine_prompt_:str="""
                Write an expansive summary of the following text delimited by triple backquotes.
                Be detailed and be sure to cover the key points of the text.
                ```{text}```
                SUMMARY:
                """):

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

if __name__ == "__main__":
    refine_summary(transcript_path=folder_template)




