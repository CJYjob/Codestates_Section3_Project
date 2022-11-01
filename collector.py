ver = '# version 1.0.0'


# 내장 모듈 임포트

# 외장 모듈 임포트

# 제작 모듈 임포트
from lib.debug_log import debug_log
from lib.collect_item_list import *
from lib.collect_daily_data import *


# 프로그램 실행
debug_log('프로그램 실행')


# 주식 종목 리스트 가져오기
    # stock_item_list() = 주식 종목 리스트를 갖는 객체
    # s.kospi_item_list = kospi 리스트
    # s.kosdaq_item_list = kosdaq 리스트
s = stock_item_list() 


# 종목별 일봉 데이터 불러오기
c = collector_daily_data()


# MySQL에 데이터 저장


