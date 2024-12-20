import pandas as pd
import os

from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
import uuid as uuid_pkg
from typing import List, Optional
from pytz import timezone
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy import delete
from sqlalchemy.types import Text, DateTime
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
    transcript:str = Field(sa_column=Column(Text))

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

class VideoStats(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    video_id: str
    publishedAt: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    channelId: str
    title: str
    description: Optional[str] = None
    thumbnails: Optional[str] = None
    channelTitle: Optional[str] = None
    tags: Optional[str] = None  # Using a list of strings for tags
    categoryId: Optional[int] = None
    viewCount: Optional[int] = None
    likeCount: Optional[float] = None
    favoriteCount: Optional[int] = None
    commentCount: Optional[int] = None
    first_day_of_month: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )

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

def df_to_sqlmodel(df: pd.DataFrame, class_i=VideoStats) -> List[SQLModel]:
    """Convert a pandas DataFrame into a a list of SQLModel objects."""
    objs = [class_i(**row) for row in df.to_dict('records')]

    with Session(engine) as session:
        session.add_all(objs)
        session.commit()

    return objs

def delete_channel_entries(channel_id_to_check: str):
    with Session(engine) as session:
        # Check if channelId exists
        exists_query = select(VideoStats).where(VideoStats.channelId == channel_id_to_check)
        result = session.exec(exists_query).first()
        
        # If channelId exists, delete all matching rows
        if result:
            delete_query = delete(VideoStats).where(VideoStats.channelId == channel_id_to_check)
            session.exec(delete_query)
            session.commit()
            print(f"All entries with channelId '{channel_id_to_check}' have been deleted.")
        else:
            print(f"No entries found with channelId '{channel_id_to_check}'.")

if __name__ == "__main__":
    dataframe = pd.read_csv('C:/Users/Ger M/Desktop/Projects/porfolio/podcastintelligence/scripts/youtubeFiles/videoStats/hasan_minhaj/pete_buttigieg_wants_to_make_america_not_suck_again.csv', index_col=0)
    
    df_to_sqlmodel(df=dataframe, class_i=VideoStats)
    
    # createEmbeddingDB(df_ = dataframe, class_info=EmbeddingTranscript, id_of_asset="SjPYwpr8ZL8")
    # createAssetDB("DrrsnFT-LNo","youtube","jd_vance_curtis_yarvin_and_the_end_of_democracy","wisecrack")