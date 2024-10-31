import pandas as pd
import os

from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
import uuid as uuid_pkg
from typing import List, Optional
from pytz import timezone
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
import datetime
from openai import AzureOpenAI
import ast

from dotenv import load_dotenv
load_dotenv()

PGHOST = os.getenv('PGHOST')
PGUSER = os.getenv('PGUSER')
PGPORT = os.getenv('PGPORT')
PGDATABASE = os.getenv('PGDATABASE')
PGPASSWORD = os.getenv('PGPASSWORD')

class assetsdb(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    id_of_asset: str
    youtube_or_rss: Optional[str]
    title_of_asset: Optional[str]
    channel_of_asset: Optional[str]

class transcriptdb(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    id_of_asset:str
    transcript:str

class EmbeddingTranscript(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    id_of_asset: str
    text: str
    n_tokens: Optional[int]
    zembeddings: List[float] = Field(sa_column=Column(Vector(1536)))

class SummaryTranscript(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    id_of_asset: str
    summary: str


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

def createAssetDB(id_of_asset:str=None, youtube_or_rss:str=None, title_of_asset:str=None, channel_of_asset:str=None):
    with Session(engine) as session:
            c = assetsdb(id_of_asset=id_of_asset,youtube_or_rss=youtube_or_rss,title_of_asset=title_of_asset,channel_of_asset=channel_of_asset)
            session.add(c)
            session.commit()


def createTranscriptDB(id_of_asset:str=None, transcriptSTR:str=None):
    with Session(engine) as session:
            c = transcriptdb(id_of_asset=id_of_asset, transcript=transcriptSTR)
            session.add(c)
            session.commit()

def createSummaryDB(id_of_asset:str=None, transcriptsummary:str=None):
    with Session(engine) as session:
            c = SummaryTranscript(id_of_asset=id_of_asset, summary=transcriptsummary)
            session.add(c)
            session.commit()


def createEmbeddingDB(df_: pd.DataFrame, class_info=None, id_of_asset:str=None, transcript:str=None):
    
    record_s = [{
    "id_of_asset":id_of_asset,
    "text":i['text'],
    "n_tokens":i['n_tokens'],
    "zembeddings":ast.literal_eval(i['ada_v2'])
    } for i in df_.to_dict('records')]

    embedding_df = [class_info(**row) for row in record_s]

    with Session(engine) as session:    
        session.add_all(embedding_df)
        session.commit()




# if __name__ == "__main__":
    # dataframe = pd.read_csv('C:/Users/Ger M/Desktop/Projects/porfolio/podcastintelligence/answers/chris_williamson/have_democrats_forgotten_about_men__richard_reeves.csv',index_col=0)
    # createEmbeddingDB(df_ = dataframe, class_info=EmbeddingTranscript, id_of_asset="SjPYwpr8ZL8")
    #  createAssetDB("DrrsnFT-LNo","youtube","jd_vance_curtis_yarvin_and_the_end_of_democracy","wisecrack")