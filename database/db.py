from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Date, Float
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
base = declarative_base()


def create_session():
    return sessionmaker(bind=engine)()


class File(base):
    __tablename__ = 'catalogue'
    file_name = Column(String, primary_key=True)


class Song(base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    artist_name = Column(String)
    title = Column(String)
    year = Column(Integer)
    release = Column(String)
    ingestion_time = Column(DateTime)


class Movie(base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    original_title = Column(String)
    original_language = Column(String)
    budget = Column(Integer)
    is_adult = Column(Boolean)
    release_date = Column(Date)
    original_title_normalized = Column(String)


class App(base):
    __tablename__ = 'apps'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    rating = Column(Float)
    version = Column(String)
    size_bytes = Column(Integer)
    is_awesome = Column(Boolean)


def database_setup():
    base.metadata.create_all(engine)


database_setup()
