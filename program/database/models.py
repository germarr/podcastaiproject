from sqlmodel import DateTime, Field, SQLModel
import uuid as uuid_pkg
from typing import List, Optional
from pytz import timezone
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy.types import Text, DateTime
import datetime
from sqlalchemy import BigInteger

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
    title_of_asset_clean: Optional[str]
    channel_of_asset: Optional[str]
    channel_of_asset_clean: Optional[str]
    channelid:Optional[str]
    channelviews:Optional[int] = Field(
        default=None, sa_column=Column(BigInteger()))
    channelsubs:Optional[int] = Field(
        default=None,sa_column=Column(BigInteger()))
    videos_published:Optional[int]=0
    upload_playlist_id:Optional[str]

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
    publishedat: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    channelid: str
    title: str
    description: Optional[str] = None
    thumbnails: Optional[str] = None
    channeltitle: Optional[str] = None
    tags: Optional[str] = None  # Using a list of strings for tags
    categoryid: Optional[int] = None
    viewcount: Optional[int] = None
    likecount: Optional[float] = None
    favoritecount: Optional[int] = None
    commentcount: Optional[int] = None
    first_day_of_month: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )

class SearchVideos(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid_pkg.UUID = Field(primary_key=True,
                                      default_factory=uuid_pkg.uuid4, index=True)
    video_id: str
    publishedat: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )
    channelid: Optional[str]= None
    title: Optional[str]= None
    description: Optional[str] = None
    thumbnails: Optional[str] = None
    channeltitle: Optional[str] = None
    tags: Optional[str] = None  # Using a list of strings for tags
    categoryid: Optional[int] = None
    viewcount: Optional[int] = None
    likecount: Optional[float] = None
    favoritecount: Optional[int] = None
    commentcount: Optional[int] = None
    first_day_of_month: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), default=datetime.datetime.now(
            timezone("America/New_York")))
    )