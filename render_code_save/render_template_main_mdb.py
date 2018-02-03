# -*- coding: utf-8 -*-
# from flask.ext.autoindex import AutoIndex
import random
import _thread
import webbrowser
import ast
from flask import Flask, render_template, request, jsonify, url_for, redirect
from fuzzyfinder import fuzzyfinder
from module_Server import uploadQiniu
from module_Server import db_process
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
# AutoIndex(app, browse_root=os.path.curdir)

img_list = []

page_title = 'Sales Dept'
html_template_path = 'index_template_pro.html'
Navbar_title = 'HGToner Sales Dept'
# navbaritems = ['主页', '信息提交', '信息查询', '表格处理']
navbaritems = ['Home', 'Info Submit', 'Info Enquiry', 'Table Process']
mdb_cfg_dict = {}

# Set Random Backgroundorder    
def Set_Random_Background(pick_number):
    img_list = []
    path = "./static/images/background/*.*"
    for fname in glob.glob(path):
        fname = re.sub(r"\\", "/", fname)
        if fname:
            img_list.append(('/'.join(fname.split('/')[2:])))

    bk_list = random.sample(set(img_list), pick_number)
    return bk_list

def open_browser (url):
    webbrowser.open_new_tab(url)
    # os.system('start ' + url)

def mdb_config_init ():
    mdb_cfg_df = db_process.exec_sql('select * from mdb_config')
    for index, row in mdb_cfg_df.iterrows():
        mdb_cfg_dict[row['name']] =  row['value_set'].split(',')
    
    mdb_cfg_dict['in_animation'] = [ str(x) for x in mdb_cfg_dict['animation'] if 'out' not in x.lower() ]
    print('-' * 20)
    print(mdb_cfg_dict['in_animation'])

    return mdb_cfg_dict

@app.route('/')
def index():
    mdb_cfg_dict = mdb_config_init()
    return render_template(html_template_path, page_content = page_content_dict['page_content'], navbaritems = navbaritems, Navbar_title = Navbar_title, navdropdown = miscellaneous['nav_dropdown_items'], nav_dropdown_button_name = miscellaneous['nav_dropdown_button_name'], page_title = page_title, mdb_cfg_dict = mdb_cfg_dict, card_items = card_items)


if __name__ == "__main__":
# information init
    with open('page_content.txt', encoding='utf-8', errors='ignore') as the_file:
        page_content_dict = ast.literal_eval(the_file.read())

    with open('miscellaneous.txt', encoding='utf-8', errors='ignore') as the_file:
        miscellaneous = ast.literal_eval(the_file.read())

    with open('card_items.txt', encoding='utf-8', errors='ignore') as the_file:
        card_items = ast.literal_eval(the_file.read())

    # print(mdb_config_init()['overlay_color'])

    bk_list = Set_Random_Background(len(page_content_dict['page_content']))
    for idx, val in enumerate(list(page_content_dict['page_content'].keys())):
        page_content_dict['page_content'][val]['bk_img_url'] = bk_list[idx]
    # app.run(host = '192.168.0.72', debug = True)
    # _thread.start_new_thread( open_browser, ('http://' + host + ':' + str(port), ) )
    host = '192.168.0.72'
    port = 5000
    app.run(debug = True, host = host, port = port)
