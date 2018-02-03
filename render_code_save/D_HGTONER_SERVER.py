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
import uploadQiniu
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
    return render_template('index.html')

@app.route('/addnumber')
def add():
    USDPrice = request.args.get('a', 0, type=float)
    url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    html = f.read().decode("utf-8")

    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)

    USDCNY = sjson["Data"][0][0][1]/10000
    RMBPrice = float(USDPrice) * float(USDCNY)/1.085

    return jsonify(result=RMBPrice)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/getsum', methods=['POST'])
def getsum():
    classifyitem = re.split(',| ', request.form['classifyitem'])
    m_sheetname = request.form['sheetname']
    sumitem = request.form['sumitem']
    print(classifyitem)
    print(m_sheetname)
    print('The types are {} {} {}'.format(type(classifyitem), type(m_sheetname), type(sumitem)))
    file_url = 'initvalue'
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df = pd.read_excel(filename, sheetname = m_sheetname)
            resfile = datetime.datetime.now().strftime('%m%d%H%M%S') + 'res.xlsx'
            df.groupby([classifyitem[0], classifyitem[1]])[sumitem].sum().reset_index().to_excel(resfile, index = False)
            file_url = uploadQiniu.UploadQNFile(resfile)
            if os.path.exists(resfile):
               os.remove(resfile)
    return r"<p><a href=" + file_url + r">点击下载处理好的文件</a></p>"

@app.route('/production_arrange', methods=['GET'])
def production_arrange():
    return '<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vSAXjxAw89v1X12A7bwc7iwWMz4VQDG9TlYgl6jmwQA0lFAnC8K7L_kptN5awbGDk0zWpnIC-zZsSN7/pubhtml?widget=true&amp;headers=false" width="1900" height="950"></iframe>'

@app.route('/table_test', methods=['GET'])
def table_test():
    df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f', 'h'],columns=['one', 'two', 'three'])
    return df.to_html()

@app.route('/getusdexchange', methods=['GET'])
def getusdexchange():
    print('in the func get exchange')
    USD_Exchage = getINFO.get_Exchange()
    USD_Exchage = '1USD = ' + str(USD_Exchage) + 'RMB'
    return jsonify(usdexchange=USD_Exchage)

@app.route('/get_TONER_NEWS', methods=['GET'])
def get_TONER_NEWS():
    # with open('TONER_NEWS.html', encoding = 'utf-8', errors='ignore') as the_file:
    with open('TONER_NEWS.html') as the_file:
       html = the_file.read()
    print(html)
    return html

if __name__ == "__main__":
    # app.run(host='106.119.88.233', debug = True)
    app.run(debug = True)

# >>> cursor.execute('select * from HGTONER where id = \'usdexchange\'')
# <sqlite3.Cursor object at 0x000001E15FA79110>
# >>> print(cursor.fetchall())
# [('usdexchange', '6.4')]
# >>> cursor.execute('update HGTONER set info=\'6.6\' where id=\'usdexchange\' ')
# <sqlite3.Cursor object at 0x000001E15FA79110>
# >>> cursor.execute('select * from HGTONER where id = \'usdexchange\'')
# <sqlite3.Cursor object at 0x000001E15FA79110>
# >>> print(cursor.fetchall())
# [('usdexchange', '6.6')]
# for idx, val in enumerate([1,2]):

