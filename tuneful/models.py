import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine

class Song(Base):
    """ The Song model:
    This should have an integer id column,
    a column specifying a one-to-one relationship with a File. """
    __tablename__ = "songs"
    id = Column(Integer, Sequence('song_id_sequence'), primary_key=True)
    info = relationship("File", uselist=False, backref="songs")

    def as_dictionary(self):
        song = {
            "id": self.id,
            "info": self.info }
        # need to add file info in here
        return song

class File(Base):
    """ The File model: This should have an integer id column
    a string column for the file name
    and the backref from the one-to-one relationship with the Song."""
    __tablename__ = "files"
    id = Column(Integer, Sequence('file_id_sequence'), primary_key=True)
    name = String(1024)
    song_id = Column(Integer, ForeignKey('songs.id'))

    def as_dictionary(self):
        file = {
            "id": self.id,
            "name": self.name }
        return file
