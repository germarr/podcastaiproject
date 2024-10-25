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

oai_auth = ''
oai_endpoint = ""

llm = AzureChatOpenAI(
    azure_endpoint=oai_endpoint,
    openai_api_key = oai_auth,
    azure_deployment='gpt-35-turbo',
    openai_api_version="2024-05-01-preview",
)

# Transcribe the audio file with timestamps
result = model.transcribe(path_to_audio)

def save_transcript(transc=None, nameOfFile:str=text_title):

    # Get the transcription text
    transcription = transc['text']

    # Define the output file path (you can modify this to your desired path)
    transcript_file_path = f"./transcript/{nameOfFile}.txt"

    # Open the file in write mode and save the transcription
    with open(transcript_file_path, "w", encoding="utf-8") as file:
        file.write(transcription)
    
    return transcript_file_path

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
    )Mike

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

    result_summary = chain({"input_documents": text}, return_only_outputs=True)

    return result_summary

transcript_file_path = save_transcript(transc=result)
result_summary = refine_summary(transcript_path=transcript_file_path)

result_summary['output_text']

