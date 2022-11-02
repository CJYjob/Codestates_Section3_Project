ver = '# version 1.0.0'

# 모듈 임포트
    ## 내장 모듈 임포트
import sys
import datetime

    ## 외장 모듈 임포트
from PyQt5.QtWidgets import *
import pymysql
import sqlalchemy

    ## 제작 모듈 임포트
from lib.debug_log import debug_log
from lib.collect_item_list import *
from lib.collect_total_data import *
from lib.db_controller import *
from lib.MySQL_config import *


# 프로그램 실행
debug_log(__name__, '프로그램 실행')


    ## MySQL connect, select database
debug_log(__name__, 'MySQL connecting')
pymysql.install_as_MySQLdb()
db = db_controller()
db.db_setting(db_name, db_id, db_passwd, db_ip, db_port)
#     ## MySQL query Example
# sql = 'CREATE DATABASE IF NOT EXISTS section3prj;'
# db.engine.execute(sql)
#     ## MySQL query 결과값 저장
# db_data = db.engine.execute(sql).fetchall()


    ## 주식 종목 리스트 가져오기
        ### stock_item_list() = 주식 종목 리스트를 갖는 객체
        ### s.kospi_item_list = kospi 리스트
        ### s.kosdaq_item_list = kosdaq 리스트
s = stock_item_list()


    ## 키움증권 OpenAPI 연결을 위한 환경 설정
app = QApplication(sys.argv)


    ## 종목별 일봉 데이터를 db에 저장
debug_log(__name__, 'MySQL store collected data')
c = collector_total_data()
data = c.run(s.kospi_item_list['code'][0], datetime.datetime.now().strftime('%Y%m%d'))

dtypesql = {"date": sqlalchemy.types.Date,
            'open': sqlalchemy.types.INTEGER,
            'high': sqlalchemy.types.INTEGER,
            'low': sqlalchemy.types.INTEGER,
            'close': sqlalchemy.types.INTEGER,
            'volume': sqlalchemy.types.INTEGER
            }

for i in range(len(s.kospi_item_list)) :
    debug_log(__name__, f'{s.kospi_item_list["code_name"][i]} DB store data, processing')
        ### 종목별 일봉 데이터를 DataFrame형태로 불러오기
    data = c.run(s.kospi_item_list['code'][i], datetime.datetime.now().strftime('%Y%m%d'))
        ### 데이터를 db에 저장(단, 데이터가 존재하는 경우, 기존 데이터를 지우고, 새 데이터로 대체)
    data.to_sql(name=s.kospi_item_list['code'][i], con=db.engine, if_exists='replace', index=False, dtype=dtypesql)







