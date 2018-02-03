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

# init database
        database_name = 'database/HGTONER_Data.db'
        conn = sqlite3.connect(database_name)
# 创建一个Cursor:
        cursor = conn.cursor()
# 继续执行一条SQL语句，插入一条记录:
# here to get all the client name
        sql_statement = 'select * from new_client_table'
        df = pd.read_sql_query(sql_statement, conn)
        client_name_list = []

# 关闭Cursor:
# database link close
        conflict_list = []
        for index, row in df.iterrows():
            if string_similar(client_data['client_company_name'],row['client_company_name']) > 0.8:
                # duplicated information
                conflict_list.append([row['account_manager_name'], row['client_company_name']])


        if len(conflict_list) == 0:
            try:
                client_data['conflict_mark'] = 'False'
                print('new client insert success!')
            except :
                ErrMsg = 'Error Msg is {}'.format(sys.exc_info()[0])
                print(ErrMsg)
                cursor.close()
                conn.commit()
                conn.close()

                return ErrMsg
        else:
            client_data['conflict_mark'] = 'True'
            print(conflict_list)

        client_data = QuoteWrap_Dict(client_data)
        insert_sql_state = "INSERT INTO {} (client_company_name,client_email,account_manager_name,information,add_date,conflict_mark)VALUES ({},{},{},{},{},{})".format('new_client_table', client_data['client_company_name'], client_data['client_email'], client_data['account_manager_name'], client_data['client_information'], 'datetime("now")', client_data['conflict_mark'])
        print(insert_sql_state)
        cursor.execute(insert_sql_state)
        cursor.close()
        conn.commit()
        conn.close()

    # show the latest 10 insert data
    sql = 'select * from new_client_table  order by add_date desc,id limit 10'
    df = SQL_Statement_2_Dataframe(sql, database_name)

    table_content = df_to_html_table(df)

    recordfile = 'record.txt'
    if os.path.exists(recordfile):
       os.remove(recordfile)

    with open('./templates/table_template_raw.html') as the_file:
       reslist = the_file.read().split('{{ table_content }}')

    final_html = reslist[0] + table_content + reslist[1]
    with open('rest.html', 'a') as the_file:
       the_file.write(final_html)
    # return final_html
    with open('./templates/tmp_html_tabel.html', 'w+') as the_file:
       the_file.write(final_html)
    return render_template('tmp_html_tabel.html')

if __name__ == "__main__":
    app.run(host='192.168.0.72', debug = True)
