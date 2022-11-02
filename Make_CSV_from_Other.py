# 모듈 임포트
    ## 내장 모듈 임포트

    ## 외장 모듈 임포트
import pymysql
import pandas as pd
from sqlalchemy import create_engine

class db_controller:
    def __init__(self):
        self.engine = None

    def db_setting(self, db_name, db_id, db_passwd, db_ip, db_port):
        # mysql 데이터베이스랑 연동하는 방식.
        self.engine = create_engine("mysql+mysqldb://" + db_id + ":" + db_passwd + "@"
                                        + db_ip + ":" + db_port + "/" + db_name, encoding='utf-8')

# db_name 이라는 변수에 우리가 조회 하고자 하는 데이터베이스의 이름을 넣는다.
db_name = 'daily_craw'
# mysql db 계정
db_id = 'root'
# mysql db ip (자신의 PC에 DB를 구축 했을 경우 별도 수정 필요 없음)
db_ip = 'localhost'  # localhost : 자신의 컴퓨터를 의미
# mysql db 패스워드
db_passwd = ''
# db port가 3306이 아닌 다른 port를 사용 하시는 분은 아래 변수에 포트에 맞게 수정하셔야 합니다.
db_port = '3306'

    ## MySQL connect, select database
pymysql.install_as_MySQLdb()
db = db_controller()
db.db_setting(db_name, db_id, db_passwd, db_ip, db_port)

# info filled in by User for MySQL controll


sql = 'SHOW TABLES;'
# db.engine.execute(sql)
table_list = db.engine.execute(sql).fetchall()

ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
result = pd.DataFrame(ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=ohlcv['date'])

for i in range(len(table_list)) :
    print(table_list[i][0], i/len(table_list)*100)
    sql = f"SELECT date, open, high, low, close, volume  FROM `{table_list[i][0]}` WHERE date > '20220101' order by date DESC;"
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