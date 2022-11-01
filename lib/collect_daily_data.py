ver = '# version 1.0.0'


# 내장 모듈 임포트
import sys

# 외장 모듈 임포트
from PyQt5.QtWidgets import *

# 제작 모듈 임포트
from lib.debug_log import debug_log
import lib.open_api as open_api


# 매일 주가 일봉 데이터를 모으는 클래스 선언
class collector_daily_data() :
    debug_log('collector_daily_data() 객체 생성')

    def init__(self) :
        
        self.api = open_api.OpenAPI()


# 모듈 테스트 코드
if __name__ == '__main__' :
    app = QApplication(sys.argv) # 키움 Open API 사용을 위한 코드
    collector_daily_data()
