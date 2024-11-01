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

import os
from dotenv import load_dotenv
load_dotenv()

openAI_key_embeddings = os.getenv('openAI_key_embeddings')
openAI_endpoint_embeddings = os.getenv('openAI_endpoint_embeddings')

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

CONNECTION_STRING = setupConnection()

engine = create_engine(CONNECTION_STRING, echo=True)

create_db_and_tables()

client = AzureOpenAI(
  api_key = openAI_key_embeddings,  
  api_version = "2023-05-15",
  azure_deployment='text-embedding-ada-002',
  azure_endpoint = openAI_endpoint_embeddings
)


def generate_embeddings(text, model="text-embedding-ada-002"): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

qs = "What is the current situation of the quarter?"

emb = generate_embeddings(text=qs)

def toDatabase(questions:str=None, answers:str=None, listOfEmb=None):

    with Session(engine) as session:
        c = chatm(question=questions, answer=answers, embedding=listOfEmb)
        session.add(c)

        session.commit()