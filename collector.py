ver = '# version 1.0.0'

# 모듈 임포트
    ## 내장 모듈 임포트
import sys
import datetime

    ## 외장 모듈 임포트
from PyQt5.QtWidgets import *
import pymysql

    ## 제작 모듈 임포트
from lib.debug_log import debug_log
from lib.collect_item_list import *
from lib.collect_total_data import *
from lib.db_controller import *
from lib.MySQL_config import *



# 프로그램 실행
debug_log(__name__, '프로그램 실행')


    ## MySQL connect
pymysql.install_as_MySQLdb()
db = db_controller()
db.db_setting(db_name, db_id, db_passwd, db_ip, db_port)
sql = 'SHOW DATABASES;'
db_data = db.engine.execute(sql).fetchall()
print(db_data)

    ## 주식 종목 리스트 가져오기
        ### stock_item_list() = 주식 종목 리스트를 갖는 객체
        ### s.kospi_item_list = kospi 리스트
        ### s.kosdaq_item_list = kosdaq 리스트
s = stock_item_list() 


    ## 키움증권 OpenAPI 연결을 위한 환경 설정
app = QApplication(sys.argv)


    ## 종목별 일봉 데이터 불러오기
c = collector_total_data()
data = c.run('005930', '20221102')
print(data)


    # MySQL에 데이터 저장


