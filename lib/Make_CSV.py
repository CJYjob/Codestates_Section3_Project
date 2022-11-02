# 모듈 임포트
    ## 내장 모듈 임포트
import os

    ## 외장 모듈 임포트
import pymysql
import sqlalchemy
import pandas as pd

    ## 제작 모듈 임포트
from lib.db_controller import *
from lib.MySQL_config import *


    ## MySQL connect, select database
pymysql.install_as_MySQLdb()
db = db_controller()
db.db_setting(db_name, db_id, db_passwd, db_ip, db_port)


sql = 'SHOW TABLES;'
# db.engine.execute(sql)
table_list = db.engine.execute(sql).fetchall()

ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
result = pd.DataFrame(ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=ohlcv['date'])

for i in range(len(table_list)) :
    sql = f"SELECT * FROM `{table_list[i][0]}`"
    data = db.engine.execute(sql).fetchall()
    ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
    for j in range(len(data)):
        date = data[j][0]
        open = data[j][1]
        high = data[j][2]
        low = data[j][3]
        close = data[j][4]
        volume = data[j][5]

        ohlcv['date'].append(date)
        ohlcv['open'].append(int(open))
        ohlcv['high'].append(int(high))
        ohlcv['low'].append(int(low))
        ohlcv['close'].append(int(close))
        ohlcv['volume'].append(int(volume))

        df = pd.DataFrame(ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=ohlcv['date'])

    df1 = df.shift(periods=-1).add_suffix('_-1_')
    df2 = df.shift(periods=-2).add_suffix('_-2_')
    df3 = df.shift(periods=-3).add_suffix('_-3_')
    df4 = df.shift(periods=-4).add_suffix('_-4_')
    df5 = df.shift(periods=-5).add_suffix('_-5_')
    df = pd.concat([df, df1, df2, df3, df4, df5], join='inner', axis=1).dropna()
    result = pd.concat([result, df])

dir_path = r'C:\Users\raona\Desktop\codestates\Section3\sprint3\s3prj\Codestates_Section3_Project\stock_5days_candle_data.csv'
result.to_csv(path_or_buf=dir_path, index=False)