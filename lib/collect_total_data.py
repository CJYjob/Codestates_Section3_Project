ver = '# version 1.0.0'


# 내장 모듈 임포트
import sys

# 외장 모듈 임포트
from PyQt5.QtWidgets import *

# 제작 모듈 임포트
from lib.debug_log import debug_log
import lib.open_api as open_api


# 매일 주가 일봉 데이터를 모으는 클래스 선언
class collector_total_data() :

    def __init__(self) :
        debug_log(__name__, 'collector_total_data() 객체 생성')
        self.api = open_api.OpenAPI()

# 데이터를 받아오는 함수
    ## get_total_data : 특정 종목의 1985년 이후 특정 날짜까지의 주가 데이터를 모두 가져오는 함수
        ### parameter 
            #### first : 종목코드 (ex.  005930 : 삼성전자 종목 코드) *종목별 코드 번호 존재
            #### second : 데이터를 가져올 최종 날짜 설정
        ### return
            #### DataFrame
                ##### open : 시작가
                ##### high : 최고가
                ##### low : 최저가
                ##### close : 종가
                ##### volumne : 거래량
    def run(self, code, start) :
        data = self.api.get_total_data(code, start)
        return data


# 모듈 테스트 코드
if __name__ == '__main__' :
    app = QApplication(sys.argv) # 키움 Open API 사용을 위한 코드
    collector_total_data()
