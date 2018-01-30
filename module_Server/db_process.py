import pandas as pd
import sqlite3
def exec_sql (sql_statement, database_name = 'database/HGTONER_Data.db'):
    conn = sqlite3.connect(database_name)
# 创建一个Cursor:
    conn.cursor().execute(sql_statement)
    res_rowcount = conn.cursor().rowcount
    conn.commit()
    conn.close()

    return res_rowcount
