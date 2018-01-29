import pandas as pd
import sqlite3
def SQL_Statement_2_Dataframe (sql_statement, database_name):
    conn = sqlite3.connect(database_name)
# 创建一个Cursor:
    df = pd.read_sql_query(sql_statement, conn)
    conn.commit()
    conn.close()

    return df
