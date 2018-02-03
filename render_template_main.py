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
import uuid
import module_Server.db_process
from flask import send_from_directory

# Set Directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir) # change to the path that you already know

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['xls', 'xlsm', 'xlsx'])
# AutoIndex(app, browse_root=os.path.curdir)

img_list = []


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

def read_text_cfg (text_cfg):
    with open(text_cfg, encoding='utf-8', errors='ignore') as the_file:
        cfg_dict = ast.literal_eval(the_file.read())

    return cfg_dict

def mdb_config_init ():
    mdb_cfg_df = db_process.exec_sql('select * from mdb_config')
    for index, row in mdb_cfg_df.iterrows():
        mdb_cfg_dict[row['name']] =  row['value_set'].split(',')

    mdb_cfg_dict['in_animation'] = [ str(x) for x in mdb_cfg_dict['animation'] if 'out' not in x.lower() ]

    return mdb_cfg_dict

@app.route('/')
def index():
    # mdb_cfg_dict = mdb_config_init()
    tab_items = read_text_cfg('tab_items.txt')['tab_items']
    return render_template(html_template_path, tab_items = tab_items)

@app.route('/excel_getsum', methods=['POST'])
def excel_getsum():
    print('excel_getsum')
    file_id = str(uuid.uuid4())
    sumitem = request.form['sumitem'].strip()
    classifyitem = [str(x).strip() for x in request.form['classifyitem'].split(',')]
    print(classifyitem)
    print(sumitem)

    if request.method == 'POST':
        try:
            upload_file = request.files['excel_sum_file']
            filename = secure_filename(upload_file.filename)
            upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_excel(filename)
            fname_no_ext, file_extension = os.path.splitext(filename)
            resfile = fname_no_ext + 'res' + file_extension

            try:
                # df.groupby([classifyitem[0], classifyitem[1]])[sumitem].sum().reset_index().to_excel(resfile, index = False)
                df.groupby(classifyitem)[sumitem].sum().reset_index().to_excel(resfile, index = False)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return 'excel 文件格式错误 或者 输入信息错误'

            # file_url = uploadQiniu.UploadQNFile(resfile)

            # if os.path.exists(filename):
               # os.remove(filename)

            # if os.path.exists(resfile):
            #    os.remove(resfile)

        except:
            print("Unexpected error:", sys.exc_info()[0])


    # return redirect(file_url)
    return send_from_directory(app.config['UPLOAD_FOLDER'],resfile, as_attachment=True)


# Submit New Client
@app.route('/new_client', methods=['GET', 'POST'])
def new_client():
    client_data = {}
    if request.method == 'POST':
        # client_data['client_company_name']  = request.form['client_company_name']
        # client_data['account_manager_name'] = request.form['account_manager_name']
        # client_data['client_email']         = request.form['client_email']
        # client_data['client_information']   = request.form['client_information']
        # client_data['conflict_mark']   = 'True'

# read upload excel data
        upload_file = request.files['new_client_file']
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        database_name = 'database/HGTONER_Data.db'
        df_new_client = pd.read_excel(filename)
        conn = sqlite3.connect(database_name)
        sql_statement = 'select * from new_client_table'
        df_clients = pd.read_sql_query(sql_statement, conn)

        for index, row in df_new_client.iterrows():
            client_data['客户公司名称']  = row['客户公司名称']
            client_data['客户经理']     = row['客户经理']
            client_data['客户邮箱']     = row['客户邮箱']
            client_data['备注信息']     = row['备注信息']
            client_data['冲突标记']     = 'True'

            # 创建一个Cursor:
            cursor = conn.cursor()
            # 继续执行一条SQL语句，插入一条记录:
            # here to get all the client name

            # 关闭Cursor:
            # database link close
            conflict_list = []
            for index, row in df_clients.iterrows():
                if string_similar(client_data['客户公司名称'],row['客户公司名称']) > 0.8:
                    # duplicated information
                    conflict_list.append([row['客户经理'], row['客户公司名称']])

            if len(conflict_list) == 0:
                try:
                    client_data['冲突标记'] = 'False'
                    print('new client insert success!')
                except :
                    ErrMsg = 'Error Msg is {}'.format(sys.exc_info()[0])
                    print(ErrMsg)
                    cursor.close()
                    conn.commit()
                    conn.close()

                    return ErrMsg
            else:
                client_data['冲突标记'] = 'True'
                print(conflict_list)

            client_data = QuoteWrap_Dict(client_data)
            insert_sql_state = """
            INSERT INTO {} (客户公司名称,客户邮箱,客户经理,备注信息,添加日期,冲突标记)VALUES ({},{},{},{},{},{})
            """.format('new_client_table', client_data['客户公司名称'], client_data['客户邮箱'], client_data['客户经理'], client_data['备注信息'], 'datetime("now")', client_data['冲突标记'])

            print(insert_sql_state)
            cursor.execute(insert_sql_state)
            cursor.close()
            conn.commit()

    conn.close()
    # show the latest 10 insert data
    sql = 'select * from new_client_table  order by 添加日期 desc,id limit 20'
    df_top_result = db_process.exec_sql(sql, database_name)

    table_content = df_to_html_table(df_top_result)

    return render_template('table_template.html', table_content = table_content)
    # return df.to_html()




if __name__ == "__main__":
#data init
    page_title = 'Sales Dept'
    html_template_path = 'index_template.html'
    Navbar_title = 'HGToner Sales Dept'
# navbaritems = ['主页', '信息提交', '信息查询', '表格处理']
    navbaritems = ['Home', 'Info Submit', 'Info Enquiry', 'Table Process']
    mdb_cfg_dict = {}

# information init
    with open('card_items.txt', encoding='utf-8', errors='ignore') as the_file:
        card_items = ast.literal_eval(the_file.read())

    # app.run(host = '192.168.0.72', debug = True)
    # _thread.start_new_thread( open_browser, ('http://' + host + ':' + str(port), ) )
    # host = '192.168.0.72'
    # port = 5000
    host = '127.0.0.1'
    port = 5000
    app.run(debug = True, host = host, port = port)
    # app.run(host = '0.0.0.0', port = '5000')
