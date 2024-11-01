### Step 1. Get assets
## ASSETSDB
## id_of_asset, youtube_or_rss, title_of_asset,channel_of_asset, timestamp

# TRANSCRIPT DB 
## id_of_asset, transcript

# TRANSCRIPT_AS_EMBEDDINGS
## id_of_asset,text,n_tokens,embeddings

# TRNASCRIPT_SUMMARY
## id_of_asset, summary



# channelid, videoid,podcastid,podcast_or_youtube,name_of_transcript,transcript
#### To get the transcript I need to go to {name_of_channel}/{name_of_chapter}

### Step 2. Get 

import os
from dotenv import load_dotenv
from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
import uuid as uuid_pkg
from typing import List, Optional
from pytz import timezone
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
import datetime
from openai import AzureOpenAI

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

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class chatm(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    questionid: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)

    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    embedding: List[float] = Field(sa_column=Column(Vector(1536)))
    question: str
    answer: str

#id_of_asset, youtube_or_rss, title_of_asset,channel_of_asset, timestamp

class assetsdb(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    timestamp: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    id_of_asset: str
    youtube_or_rss: Optional[str]
    title_of_asset: Optional[str]
    channel_of_asset: Optional[str]

CONNECTION_STRING = setupConnection()
engine = create_engine(CONNECTION_STRING, echo=True)

create_db_and_tables()

def sendToDB(questions:str=None, answers:str=None, listOfEmb=None):

    with Session(engine) as session:
        c = chatm(question=questions, answer=answers, embedding=listOfEmb)
        session.add(c)

        session.commit()







