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

@app.route("/api/songs", methods=["PUT"])
def songs_put():
    data = json.dumps([])
    return Response(data, 200, mimetype="application/json")