from sqlmodel import DateTime, Field, SQLModel, create_engine, Session, select
import os
import ast
from .models import assetsdb
from sqlalchemy import delete

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
