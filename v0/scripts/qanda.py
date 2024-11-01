import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.embeddingsToDB import generate_embeddings, answersExample,transcriptExample, questionsExample, llm, transcriptToTokens
import numpy as np
import pandas as pd
import ast
import argparse
from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
from scripts.backend.todb import toDatabase

# Initialize the argument parser
parser = argparse.ArgumentParser(description="Process some input.")

# Add the --input argument
parser.add_argument('--input', type=str, required=True, help="The input string to be processed")

# Parse the arguments
args = parser.parse_args().input

queryFromUser = args 

questionsExample = os.getenv('questionsExample')

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_docs(df, user_query, top_n=4):
    embedding = generate_embeddings(
        user_query,
        model="text-embedding-ada-002" # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )

    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(ast.literal_eval(x), embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )

    fullanswer = " ".join(res['text'].to_list())

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=10)
    # cook = Document(page_content=fullanswer)
    # # text = text_splitter.split_documents([cook])

    response = llm(
    messages=[
        {"role": "user", "content": f'Answer any question using ONLY this data: {fullanswer}'},
        {"role": "system", "content": user_query}
        ]
    )

    toDatabase(questions=user_query, answers=response.content, listOfEmb=embedding)

    return {'q':user_query, 'ans':response.content}

def sendQToDb(ans_dict=None, file_path=None):
        
        answerDF = pd.DataFrame([ans_dict])
        
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        
        # Open the file in append mode
        with open(file_path, "a", encoding="utf-8") as file:
            if not file_exists:
                # If the file doesn't exist, write the headers and the first row
                answerDF.to_csv(file, index=False, header=True, lineterminator='\n')
            else:
                # If the file exists, only append the row without headers
                answerDF.to_csv(file, index=False, header=False, lineterminator='\n')



if __name__ == '__main__':
     transcriptToTokens(transcript_path=transcriptExample, pathToCSV=answersExample)
     dataframeWAnswers = pd.read_csv(answersExample)
     answerT = search_docs(df=dataframeWAnswers, user_query= queryFromUser)
     sendQToDb(ans_dict=answerT, file_path=questionsExample)