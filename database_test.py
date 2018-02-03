# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
conn = sqlite3.connect(r'D:\MyPython\HGToner_Web_Server\database\HGTONER_Data.db', timeout=10)

df = pd.read_excel("data\新客户模板.xlsx")

df.to_sql('new_client_table', conn, if_exists='append')

conn.close()
