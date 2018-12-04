#!/bin/bash
pyinstaller -w -F --hidden-import=flask_api.parsers --hidden-import=flask_api.renderers --hidden-import=sklearn.neighbors.typedefs --hidden-import=email.mime.application --hidden-import=email.mime.audio --hidden-import=email.mime.base --hidden-import=email.mime.image --hidden-import=email.mime.message --hidden-import=email.mime.multipart --hidden-import=email.mime.nonmultipart --hidden-import=email.mime.text run_folder_predictor.py

pyinstaller -w -F run_folder_predictor.spec
