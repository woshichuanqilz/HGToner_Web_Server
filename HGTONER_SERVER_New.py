# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, url_for, redirect
import re
import json
import urllib.request
import os
import socket
from werkzeug import secure_filename
import pandas as pd
import pypinyin
import datetime
import numpy as np
import sys
import time
from fuzzyfinder import fuzzyfinder
import module_Server.uploadQiniu
import getINFO

# Set Directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # change to the path that you already know

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['xls', 'xlsm', 'xlsx'])

@app.route('/')
def index():
    # return render_template('index.html', USD_Exchange = getINFO.get_Exchange())
    return render_template('index.html', USD_Exchange = '6.3')

if __name__ == "__main__":
    # app.run(host='106.119.88.233', debug = True)
    app.run(debug = True)
