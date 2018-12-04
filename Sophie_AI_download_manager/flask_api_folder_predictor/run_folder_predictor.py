#!/usr/bin/env python

from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

# from flask import request
# from flask import render_template
# from flaskexample import app
# from sqlalchemy import create_engine
# from sqlalchemy_utils import database_exists, create_database
# import pandas as pd
#import psycopg2
from predict_Model import ModelIt

@app.route("/", methods=['GET','POST'])
def notes_list():
    """
    get filename, file_path_input, and run python model, return the folder name
			data: {file_name: file_name,
						 root_dir: root_dir,
						 downloads_dir: downloads_dir
						},

    """

    if request.method == 'POST':
        file_name = request.data['file_name']
        root_dir = request.data['root_dir']
        downloads_dir = request.data['downloads_dir']

        return ModelIt(file_name, root_dir, downloads_dir)
    if request.method == 'GET':
        return 'random_folder ^.^'


# @app.route("/", methods=['GET', 'POST'])
# def notes_list():
#     """
#     List or create notes.
#     """
#     if request.method == 'POST':
#         note = str(request.data.get('text', ''))
#         idx = max(notes.keys()) + 1
#         notes[idx] = note
#         return note_repr(idx), status.HTTP_201_CREATED
#
#     # request.method == 'GET'
#     return [note_repr(idx) for idx in sorted(notes.keys())]


# @app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
# def notes_detail(key):
#     """
#     Retrieve, update or delete note instances.
#     """
#     if request.method == 'PUT':
#         note = str(request.data.get('text', ''))
#         notes[key] = note
#         return note_repr(key)
#
#     elif request.method == 'DELETE':
#         notes.pop(key, None)
#         return '', status.HTTP_204_NO_CONTENT
#
#     # request.method == 'GET'
#     if key not in notes:
#         raise exceptions.NotFound()
#     return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)
