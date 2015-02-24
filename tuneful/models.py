import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *

class Song(Base):
    __tablename__  = "songs"
    """ The Song model: This should have an integer id column,
    a column specifying a one-to-one relationship with a File. """
    id = Column(Integer, Sequence('id'), primary_key=True)
    name = Column(String(250), nullable=False)
    song_file = relationship("File",
        uselist=False,
        backref="songs" )

    def __repr__(self):
        # was return str(self.as_dictionary() )
        return str("<<" + self.as_dictionary() + ">>")

    def as_dictionary(self):
        song = {
            "id": self.id,
            "file_name": self.song_file.file_name
        }
        return song

class File(Base):
    __tablename__ = "files"
    """ The File model: This should have an integer id column
    a string column for the file name and the backref from the one-to-one relationship with the Song."""
    id = Column(Integer, primary_key=True)
    file_name = Column(String(1024) )
    song_id = Column(Integer, ForeignKey('songs.id'))
    # song_info = relationship("Song", backref="files")

    def __repr__(self):
        # was return str(self.as_dictionary() )
        return str(self.as_dictionary())

    def as_dictionary(self):
        file = {
            "id": self.id,
            "file_name": self.file_name,
            "path": url_for("uploaded_file", filename=self.file_name)
        }
        return file

# engine = create_engine("postgresql://:@localhost:5432/tuneful")
# session = sessionmaker(bind=engine)()
# Base.metadata.drop_all(engine) #---start with a fresh database
# Base.metadata.create_all(engine)
# Base = declarative_base()
#
# er   = Song(name="Eleanor Rigby")
# nw   = Song(name="Norwegian Wood")
# ytd  = Song(name="Yesterday")
# ditl = Song(name="Day in the Life")
# hlp  = Song(name="Help!")
#
#
# session.add_all([er, nw, ytd, ditl, hlp])
# session.commit()
#
# sf = [ File(file_name="foo0.mp4", song_id=er.id)
#     , File(file_name="foo1.mp4", song_id=nw.id)
#     , File(file_name="foo2.mp4", song_id=ytd.id)
#     , File(file_name="foo3.mp4", song_id=ditl.id)
#     , File(file_name="foo4.mp4", song_id=hlp.id)
# ]
#
# session.add_all(sf)
# session.commit()