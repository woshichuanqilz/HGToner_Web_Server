# -*- coding: utf-8 -*-
import sqlite3
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
from module_Server import uploadQiniu
import getINFO
from module_Server.string_process import *
from module_Server.db_process import *
from module_Server.html_process import *
import uuid

# Set Directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # change to the path that you already know

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['xls', 'xlsm', 'xlsx'])

@app.route('/')
def index():
    return render_template('new_client.html')

@app.route('/submit_new_client', methods=['POST'])
def submit_new_client():
    client_data = {}
    if request.method == 'POST':
        client_data['client_company_name']  = request.form['client_company_name']
        client_data['account_manager_name'] = request.form['account_manager_name']
        client_data['client_email']         = request.form['client_email']
        client_data['client_information']   = request.form['client_information']
        client_data['conflict_mark']   = 'True'
    return redirect(url_for('get_new_client_info', uuid = str(uuid.uuid4())))

@app.route('/get_new_client_info/<uuid>')
def get_new_client_info(uuid):
    database_name = 'database/HGTONER_Data.db'
    sql = 'select * from new_client_table  order by add_date desc,id limit 10'
    df = SQL_Statement_2_Dataframe(sql, database_name)

    table_content_info = df_to_html_table(df)

    return render_template('table_template.html', table_content = table_content_info)

if __name__ == "__main__":
    app.run(host='192.168.0.72', debug = True)
