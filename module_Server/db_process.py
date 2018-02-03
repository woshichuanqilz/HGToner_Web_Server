import pandas as pd
import sqlite3
import os
def exec_sql (sql_statement, database_name = 'database/HGTONER_Data.db'):
    conn = sqlite3.connect(database_name)
# 创建一个Cursor:
    cursor = conn.cursor()
    if 'select' in sql_statement:
        result = pd.read_sql(sql_statement, conn)
    else:
        result = cursor.execute(sql_statement)

    conn.commit()
    conn.close()

    return result



if __name__ == '__main__':
    # print(exec_sql('select * from mdb_config', database_name = '../database/HGTONER_Data.db'))
    print(exec_sql('select value_set from mdb_config where name = \'overlay_color\'', database_name = '../database/HGTONER_Data.db')['value_set'].to_string(index = False))
