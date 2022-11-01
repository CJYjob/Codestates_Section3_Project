ver = '# version 1.0.0'


# 내장 모듈 임포트
import sys
import time

# 외장 모듈 임포트
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame

# 제작 모듈 임포트
from lib.debug_log import debug_log


# 환경 확인 
is_64bits = sys.maxsize > 2**32
if is_64bits:
    debug_log('64bit 환경입니다.')
else:
    debug_log('32bit 환경입니다.')


# 상수 변수 선언
    # TR_request_interval
        # 키움증권 조회 차단 회피용 지연 시간 설정
        # TR 5건 이하 - time.sleep없이 그냥 진행가능
        # TR 100건 이하 - time.sleep(0.2)를 추가하여 진행가능
        # TR 1000건 이하 - time.sleep(1.8)을 추가하여 진행가능
        # TR 1000건 초과 - 1시간 1000건 제약으로 time.sleep(3.6)을 추가하여 진행가능
TR_request_interval = 3.6 


# 키움증권 OpenAPI와 통신하기 위한 클래스 선언
class Openapi(QAxWidget):
    debug_log('Openapi() 객체 생성')

    def __init__(self) :
        super().__init()
        self._create_open_api_handler()
        self._set_signal_slots()
        self.comm_connect()
        self.account_info()


    # 키움증권 Open API 핸들링 객체 생성
    def _create_open_api_handler() :
        try :
            debug_log('OpenAPI 핸들링 객체 생성 성공')
            self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        except Exception() as e :
            debug_log(e)


    # Open API의 signal slot 셋팅
    def _set_signal_slots() :
        try:
            debug_log('signal-event slot 생성')
            self.OnEventConnect.connect(self._event_connect)
            self.OnReceiveTrData.connect(self._receive_tr_data)
            self.OnReceiveMsg.connect(self._receive_msg)
            # 주문체결 시점에서 키움증권 서버가 발생시키는 OnReceiveChejanData 이벤트를 처리하는 메서드
            self.OnReceiveChejanData.connect(self._receive_chejan_data)
        except Exception as e:
            is_64bits = sys.maxsize > 2**32
            if is_64bits:
                debug_log('현재 Anaconda는 64bit 환경입니다. 32bit 환경으로 실행하여 주시기 바랍니다.')
            else:
                debug_log(e)


    # signal function

    # OpenAPI 로 로그인 명령(CommConnect())전달 후 Event loop 생성
    def comm_connect(self) :
        try :
            debug_log('CommConnect()-event loop 생성')
            self.dynamicCall('CommConnect()')
            time.sleep(TR_request_interval)
            self.login_event_loop = QEventLoop()
            self.login_event_loop.exec_()
        except Exception as e :
            debug_log(e)


    # event function
    def _event_connect(self, err_code) :
        try : 
            if err_code == 0 :
                debug_log('Connect Success')
            else :
                debug_log(f'Connect fail. errCode : {err_code}')
        except Exception as e :
            debug_log(e)

# 모듈 테스트 코드
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Openapi()