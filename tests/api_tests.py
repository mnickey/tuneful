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
from pprint import pprint as pp

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
        # Create the file and the song
        fileA = models.File(name="test")
        songA = models.Song(info=fileA)
        # Add the song to the database
        session.add_all([songA, fileA])
        session.commit()
        # Check to make sure that the song is seen by the endpoint
        response = self.client.get("/api/songs",
                    headers = [("Accept", "application/json")] )

        # Check that the status_code is accepted (200)
        self.assertEqual(response.status_code, 200)

        # Check to make sur ethat the mimetype is JSON
        self.assertEqual(response.mimetype, "application/json")

        # print out the song and file details if there is a failure
        # using assert False
        # pp ("songA details: " + str(songA) )
        # pp ("fileA details: " + str(fileA) )
        # assert False
        self.assertEqual(songA.id, 1)
    def testPostSongs(self):
        """ Post a song """
        # Create the file and the song
        fileA = models.File(name="testPut")
        songA = models.Song(info=fileA)
        # Add the song to the database
        session.add_all([songA, fileA])
        session.commit()
        # Check to make sure that the song is seen by the endpoint
        response = self.client.put("api/songs",
                    headers = [("application/json")] )
        pp ("songA details: " + str(songA) )
        pp ("fileA details: " + str(fileA) )
        #assert False
        self.assertEqual(songA.id, 1)

