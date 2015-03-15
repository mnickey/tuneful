import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

@app.route("/api/songs", methods=["GET"])
def songs_get():
    """ Get a list of songs """
    print "/api/songs method: GET"
    my_songs =  session.query(models.Song).all()
    print "My Songs from /api/songs GET: ", repr(my_songs)
    try:
        # print json.dumps(json.loads('[{"file_name": "chords.wav", "id": 29}]') )
        # print "JDumps", json.dumps(my_songs)
        return Response(repr(my_songs), 200, mimetype="application/json")
    except:
        print "Got a type error... wheee"
        return ""
    finally:
        pass

@app.route("/api/songs/<int:id>", methods=["PUT", "POST", "DELETE"])
@decorators.accept("application/json")
def songs_put(id):
    """ Put a song into the database """
    print "/api/songs<int:id> method: PUT, POST & DELETE"
    pass

# create a post route and get the id for the song posted
@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    # Requires: Song name, file_name and upload URL
    print "/api/songs method: POST"
    print "Request.args: ", request.args.items()
    print "Request.data: ", repr(request.data)
    data_json = json.loads(request.data)

    print "Request.data FILE: ", data_json["file"]
    f_info = session.query(models.File).filter(models.File.id==data_json["file"]["id"]).one()
    print "f_info: ", f_info
    song = models.Song(name = f_info.file_name, song_id=f_info.id )
    session.add(song)
    session.commit()
    return Response('', 200)

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    print "/uploads/<filename> method: GET"
    return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    print "/api/files method: POST"
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    print "Line 53, filename: ", filename
    db_file = models.File(file_name=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
    # return Response('', 200)

