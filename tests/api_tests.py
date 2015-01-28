import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()
        # Set up the tables in the database
        Base.metadata.create_all(engine)
        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        # Delete test upload folder
        shutil.rmtree(upload_path())
    def testGetSongs(self):
        """ Get a song from a prepopulated database """
        songA = models.Song(id=1) # Need to figure out how to add file info in here.
        session.add_all([songA])
        session.commit()
        self.assertEqual(songA.id, 1)
    def testPostSongs(self):
        """ Post a song """
        pass
