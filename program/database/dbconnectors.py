from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
import os
import ast
from .models import SearchVideos,VideoStats,assetsdb,transcriptdb,SummaryTranscript,EmbeddingTranscript
from sqlalchemy import delete
import pandas as pd
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()

PGHOST = os.getenv('PGHOST')
PGUSER = os.getenv('PGUSER')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')
PGPASSWORD = os.getenv('PGPASSWORD')

def setupConnection():
    hostName = PGUSER
    password = PGPASSWORD
    host = PGHOST
    port = PGPORT
    db_name = PGDATABASE

    db_url = f'postgresql://{hostName}:{password}@{host}:{port}/{db_name}'

    return db_url

def create_db_and_tables(e):
    SQLModel.metadata.create_all(e)

CONNECTION_STRING = setupConnection()
engine = create_engine(CONNECTION_STRING, echo=True)

create_db_and_tables(e=engine)

def createAssetDB(channelid:str=None,channel_of_asset_clean:str=None,title_of_asset_clean:str=None, id_of_asset:str=None, youtube_or_rss:str=None, title_of_asset:str=None, channel_of_asset:str=None):
    with Session(engine) as session:
            exists_query = select(assetsdb).where(assetsdb.id_of_asset == id_of_asset)
            result = session.exec(exists_query).first()
            
            if result:
                delete_query = delete(assetsdb).where(assetsdb.id_of_asset == id_of_asset)
                session.exec(delete_query)
                session.commit()

            c = assetsdb(channelid=channelid,
                         channel_of_asset_clean=channel_of_asset_clean,
                         title_of_asset_clean=title_of_asset_clean,
                         id_of_asset=id_of_asset,
                         youtube_or_rss=youtube_or_rss,
                         title_of_asset=title_of_asset,
                         channel_of_asset=channel_of_asset)
            session.add(c)
            session.commit()

def createTranscriptDB(id_of_asset:str=None, transcriptSTR:str=None):
    with Session(engine) as session:
            
            exists_query = select(transcriptdb).where(transcriptdb.id_of_asset == id_of_asset)
            result = session.exec(exists_query).first()

            if result:
                delete_query = delete(transcriptdb).where(transcriptdb.id_of_asset == id_of_asset)
                session.exec(delete_query)
                session.commit()
            
            c = transcriptdb(id_of_asset=id_of_asset, transcript=transcriptSTR)
            session.add(c)
            session.commit()

def createSummaryDB(id_of_asset:str=None, transcriptsummary:str=None):
    with Session(engine) as session:
        exists_query = select(SummaryTranscript).where(SummaryTranscript.id_of_asset == id_of_asset)
        result = session.exec(exists_query).first()

        if result:
            delete_query = delete(SummaryTranscript).where(SummaryTranscript.id_of_asset == id_of_asset)
            session.exec(delete_query)
            session.commit()

        c = SummaryTranscript(id_of_asset=id_of_asset, summary=transcriptsummary)
        session.add(c)
        session.commit()

def createEmbeddingDB(df_: pd.DataFrame, class_info=EmbeddingTranscript, id_of_asset:str=None, transcript:str=None):
    
    record_s = [{
    "id_of_asset":id_of_asset,
    "text":i['text'],
    "n_tokens":i['n_tokens'],
    "zembeddings":ast.literal_eval(i['ada_v2'])
    } for i in df_.to_dict('records')]

    embedding_df = [class_info(**row) for row in record_s]

    with Session(engine) as session:
        exists_query = select(class_info).where(class_info.id_of_asset == id_of_asset)
        result = session.exec(exists_query).first()

        if result:
            delete_query = delete(class_info).where(class_info.id_of_asset == id_of_asset)
            session.exec(delete_query)
            session.commit()

        session.add_all(embedding_df)
        session.commit()

def df_to_sqlmodel(df: pd.DataFrame, class_i=VideoStats, id_of_asset:str=None) -> List[SQLModel]:
    """Convert a pandas DataFrame into a a list of SQLModel objects."""
    objs = [class_i(**row) for row in df.to_dict('records')]
    
    with Session(engine) as session:
        if id_of_asset != None:
            exists_query = select(class_i).where(class_i.id_of_asset == id_of_asset)
            result = session.exec(exists_query).first()
            
            if result:
                delete_query = delete(class_i).where(class_i.id_of_asset == id_of_asset)
                session.exec(delete_query)
                session.commit()
            
        session.add_all(objs)
        session.commit()

    return objs

def delete_channel_entries(channel_id_to_check: str,class_i=VideoStats):
    with Session(engine) as session:
        # Check if channelId exists
        exists_query = select(class_i).where(class_i.channelId == channel_id_to_check)
        result = session.exec(exists_query).first()
        
        # If channelId exists, delete all matching rows
        if result:
            delete_query = delete(class_i).where(class_i.channelId == channel_id_to_check)
            session.exec(delete_query)
            session.commit()
            print(f"All entries with channelId '{channel_id_to_check}' have been deleted.")
        else:
            print(f"No entries found with channelId '{channel_id_to_check}'.")



# def delete_channel_entries(channel_id_to_check: str):
#     with Session(engine) as session:
#         # Check if channelId exists
#         exists_query = select(VideoStats).where(VideoStats.channelId == channel_id_to_check)
#         result = session.exec(exists_query).first()
        
#         # If channelId exists, delete all matching rows
#         if result:
#             delete_query = delete(VideoStats).where(VideoStats.channelId == channel_id_to_check)
#             session.exec(delete_query)
#             session.commit()
#             print(f"All entries with channelId '{channel_id_to_check}' have been deleted.")
#         else:
#             print(f"No entries found with channelId '{channel_id_to_check}'.")
