ver = '# version 1.0.0'

# 내장 모듈 임포트

# 외장 모듈 임포트

# 제작 모듈 임포트
from lib.debug_log import debug_log
from lib.get_item_list import *

debug_log(__name__ + ver, '프로그램 실행')

# 주식 종목 정보 가져오기

s = StockItem()
s.code_df_kospi
s.code_df_kosdaq

