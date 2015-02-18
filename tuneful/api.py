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

@app.route("/api/files", methods=["POST"])
def songs_post():
    file = request.files["file"]
    fileB = models.File(file_name=file.filename)
    # print file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    songB = models.Song(name=file.filename, song_file = fileB )
    session.add_all([songB])
    session.commit()
    # print request.files["file"]
    return Response('', 200 )

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
    elif request.method == "POST":
        song = session.query(models.Song).get(id)
        session.add(song)
        session.commit()
        song = session.query(models.Song).get(id)
        return Response('', 200, mimetype="application/json")
    else:
        print "wtf!?!"
        return Response('', 500, mimetype="application/json")
@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)
