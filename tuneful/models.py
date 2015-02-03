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
    file_id = (Column, Integer, ForeignKey('files.id'))
    info = relationship("File", uselist=False, backref="songs")

    def __repr__(self):
        # was return str(self.as_dictionary() )
        return ("[[[" + str(self.as_dictionary()) + "]]]")

    def as_dictionary(self):
        song = {
            "id": self.id,
            "info": self.info }
        # print "This is song.info: ", self.info.as_dictionary()
        return song

class File(Base):
    """ The File model: This should have an integer id column
    a string column for the file name
    and the backref from the one-to-one relationship with the Song."""
    __tablename__ = "files"
    id = Column(Integer, Sequence('file_id'), primary_key=True)
    name = String(1024)
    song_id = Column(Integer, ForeignKey('songs.id'))
    song_info = relationship("Song", uselist=False, backref="files")

    def __repr__(self):
        # was return str(self.as_dictionary() )
        return ("[[[" + str(self.as_dictionary()) + "]]]")

    def as_dictionary(self):
        file = {
            "id": self.id,
            "name": self.name }
        return file
