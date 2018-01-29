# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, url_for, redirect
from fuzzyfinder import fuzzyfinder
from module_Server import uploadQiniu
from module_Server.db_process import *
from module_Server.html_process import *
from module_Server.string_process import *
from os.path import basename
from werkzeug import secure_filename
import datetime
import getINFO
import glob
import json
import numpy as np
import os
import pandas as pd
import pathlib
import pypinyin
import re
import socket
import sqlite3
import sys
import time
import urllib.request

# Set Directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # change to the path that you already know

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['xls', 'xlsm', 'xlsx'])

img_list = []
path = "static/images/gallery/*"
# for fname in glob.glob(path):
    # img_file_path = '/'.join(str(x) for x in fname.replace('\\', '/').split('/')[1:])
    # img_description = os.path.splitext(basename(img_file_path))[0]
    # an_item = {'img_src':img_file_path, 'img_description' : img_description }
    # img_list.append(an_item)

for fname in glob.glob(path):
    img_file_path = '/'.join(str(x) for x in fname.replace('\\', '/').split('/')[1:])
    img_description = os.path.splitext(basename(img_file_path))[0]
    an_item = {'img_src':img_file_path, 'img_description' : img_description }
    img_list.append(an_item)

mydict_fluid = {'title' : 'HGToner Sales Dept. Moments',
          'main_header' : 'HGToner Sales Dept. Moments',
          'main_description' : 'Time Pass By, Love Goes On',
          'img_list' : img_list
         }

mydict_thumbnail = {'title' : 'HGToner Sales Dept. Moments',
                  'main_header' : 'HGToner Sales Dept. Moments',
                  'main_description' : 'Time Pass By, Love Goes On',
                  'img_list' : img_list
                 }

html_template_path = 'gallery_thumbnail.html'

    # return temp

@app.route('/')
def index():
    return render_template(html_template_path, title = mydict_thumbnail['title'], main_header = mydict_thumbnail['main_header'], main_description = mydict_thumbnail['main_description'], img_list = mydict_thumbnail['img_list'])

@app.route('/test/<name>')
def show_name(name):
    return name

if __name__ == "__main__":
    app.run(debug = True)
