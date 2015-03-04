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
    data = json.dumps([])
    return Response(data, 200, mimetype="application/json")

# @app.route("/api/files", methods=["POST"])
# @decorators.require("multipart/form-data")
# @decorators.accept("application/json")
# def songs_post():
#     file = request.files["file"]
#     fileB = models.File(file_name=file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#     songB = models.Song(name=file.filename, song_file = fileB )
#     session.add_all([songB])
#     session.commit()
#     data = songB.as_dictionary()
#     print(type(data))
#     print(data)
#     return Response(
#         (data) ,
#         201, mimetype="application/json" )

@app.route("/api/songs/<int:id>", methods=["PUT", "POST", "DELETE"])
@decorators.accept("application/json")
def songs_put(id):
    """ Put a song into the database """
    if request.method == "DELETE":
        song = session.query(models.Song).get(id)
        session.delete(song)
        session.commit()
        return Response('', 200, mimetype="application/json")
    elif request.method == "PUT":
        song = session.query(models.Song).get(id)
        session.add(song)
        session.commit()
        song = session.query(models.Song).get(id)
        return Response('', 200, mimetype="application/json")
    # elif request.method == "POST":
    #     song = session.query(models.Song).get(id)
    #     session.add(song)
    #     session.commit()
    #     song = session.query(models.Song).get(id)
    #     return Response('', 200, mimetype="application/json")
    else:
        print "wtf!?!"
        return Response('', 500, mimetype="application/json")

# create a post route and get the id for the song posted
@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
def songs_post():
    # Requires: Song name, file_name and upload URL
    print "At entry songs_post" , request.json
    # provides:
    #   a response code 200 to show that it worked
    #   a new song has to be in the database/songs table linked to the right file in the File table.
    file_o = request.files.get('file')
    print "REQUEST FILES: ", request
    print "file_o info: ", file_o
    file_n = secure_filename(file_o.filename)
    # so at this point you have a secure filename
    song_n = request.json # need this from request.json somehow
    print "This is song_n: ", song_n
    #  at this point song_n is a song name
    #  at this point you know what you need
    file = models.File(file_name=file_n) # This satisfies p(1)
    # and add to db and save
    # and upload the file # this satisfies p(2)
    file_o.save(upload_path())
    song = models.Song(name=secure_filename(file_o.file_name)) # this p(3)
    # now add and commit your song.
    session.add(song)
    session.commit()
    # provide 200 status code, AND (1) new File row in Files table
    # (2) file uploaded to UPLOADS folder.
    # (3) new song row added to Songs table

    return Response("",200) # satisfies return code

    # return Response('', 200, mimetype="application/json")

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    print "In File_post: ", request.json
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    print "Line 88, filename: ", filename
    db_file = models.File(file_name=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
