ver = '# version 1.0.0'

# 모듈 임포트
    ## 내장 모듈 임포트
import sys
import time

    ## 외장 모듈 임포트
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame

    ## 제작 모듈 임포트
from lib.debug_log import debug_log


# 환경 확인 
is_64bits = sys.maxsize > 2**32
if is_64bits:
    debug_log(__name__, '64bit 환경입니다.')
else:
    debug_log(__name__, '32bit 환경입니다.')


# 상수 변수 선언
    ## TR_request_interval
        ### 키움증권 조회 차단 회피용 지연 시간 설정
        ### TR 5건 이하 - time.sleep없이 그냥 진행가능
        ### TR 100건 이하 - time.sleep(0.2)를 추가하여 진행가능
        ### TR 1000건 이하 - time.sleep(1.8)을 추가하여 진행가능
        ### TR 1000건 초과 - 1시간 1000건 제약으로 time.sleep(3.6)을 추가하여 진행가능
TR_request_interval = 0.2


# 키움증권 OpenAPI와 통신하기 위한 클래스 선언
class OpenAPI(QAxWidget):
    
    def __init__(self) :
        debug_log(__name__, 'Openapi() 객체 생성')
        super().__init__()
        self._create_open_api_handler()
        self._set_signal_slots()
        self.comm_connect()
        self.account_info()


# 키움증권 Open API 핸들링 객체 생성
    def _create_open_api_handler(self) :
        try :
            debug_log(__name__, 'OpenAPI 핸들링 객체 생성 성공')
            self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        except Exception() as e :
            debug_log(__name__, e)


# Open API의 signal slot 셋팅
    def _set_signal_slots(self) :
        try:
            debug_log(__name__, 'signal-event slot 생성')
            self.OnEventConnect.connect(self._event_connect)
            self.OnReceiveTrData.connect(self._receive_tr_data)
            self.OnReceiveMsg.connect(self._receive_msg)
            # 주문체결 시점에서 키움증권 서버가 발생시키는 OnReceiveChejanData 이벤트를 처리하는 메서드
            self.OnReceiveChejanData.connect(self._receive_chejan_data)
        except Exception as e:
            is_64bits = sys.maxsize > 2**32
            if is_64bits:
                debug_log(__name__, '현재 Anaconda는 64bit 환경입니다. 32bit 환경으로 실행하여 주시기 바랍니다.')
            else:
                debug_log(__name__, e)


# signal function

    ## OpenAPI 로 로그인 명령(CommConnect())전달 후 Event loop 생성
    def comm_connect(self) :
        try :
            debug_log(__name__, 'CommConnect()-event loop 생성')
            self.dynamicCall('CommConnect()')
            time.sleep(TR_request_interval)
            self.login_event_loop = QEventLoop()
            self.login_event_loop.exec_()
        except Exception as e :
            debug_log(__name__, e)

    ## 로그인 정보 확인 함수
    def get_login_info(self, tag) :
        try :
            debug_log(__name__, "로그인 정보 호출 함수")
            info = self.dynamicCall('GetLoginInfo(QString)', tag)
            time.sleep(TR_request_interval)
            return info
        except Exception as e :
            debug_log(__name__, e)

    ## Open API TR 인자 셋팅 함수
    def set_input_value(self, id, value) :
        debug_log(__name__, f'TR의 {id}를 {value}로 설정')
        try :
            self.dynamicCall('SetInputValue(QString, QString', id, value)
        except Exception as e :
            debug_log(__name__, e)

    ## openAPI 의 CommRqData() 함수 사용
    def comm_rq_data(self, rqname, trcode, next, screen_no):
        debug_log(__name__, f"CommRqData({rqname}, {trcode}, {next}, {screen_no})")
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        time.sleep(TR_request_interval)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    ## TR 반복 회수 반환 함수
    def _get_repeat_cnt(self, trcode, rqname) :
        debug_log(__name__, 'TR 반복 수 확인 signal 함수')
        try :
            ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
            return ret
        except Exception as e:
            debug_log(__name__, e)

    ## TR data 수령 함수
    def _get_comm_data(self, code, field_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", code, field_name, index, item_name)
        return ret.strip()


# event function

    ## OpenAPI 로그인 명령에 대한 event 처리 함수
    def _event_connect(self, err_code) :
        try : 
            if err_code == 0 :
                debug_log(__name__, 'Connect Success')
            else :
                debug_log(__name__, f'Connect fail. errCode : {err_code}')
            self.login_event_loop.exit()
        except Exception as e :
            debug_log(__name__, e)

    ## OpenAPI CommRqData() 명령에 대한 event 처리 함수
    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        debug_log(__name__, f"_receive_tr_data(rqname={rqname}, trcode={trcode}, next={next}) 호출")
        
        ### TR 데이터가 남았는지 여부를 나타내는 flag
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        ### opt10081 TR에 대한 처리 함수 호출.
        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        ### TR 회신 후 event_loop 종료
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass


# TR function

    ## CommRqData()로 전달된 opt10081 TR 처리 함수
    def _opt10081(self, rqname, trcode):
        debug_log(__name__, 'opt10081 TR 처리 함수 시작')

        # 몇번 반복 실행 할지 설정
        ohlcv_cnt = self._get_repeat_cnt(trcode, rqname)

        # 하나의 row씩 append
        for i in range(ohlcv_cnt):
            date = self._get_comm_data(trcode, rqname, i, "일자")
            open = self._get_comm_data(trcode, rqname, i, "시가")
            high = self._get_comm_data(trcode, rqname, i, "고가")
            low = self._get_comm_data(trcode, rqname, i, "저가")
            close = self._get_comm_data(trcode, rqname, i, "현재가")
            volume = self._get_comm_data(trcode, rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))


# 계좌 번호 확인 함수
    def account_info(self) :
        account_number = self.get_login_info('ACCNO')
        self.account_number = account_number.split(';')[0]
        debug_log(__name__, '계좌번호 : ' + self.account_number)


# 특정 종목의 일자별 거래 데이터 조회 함수
    ## parameter
        ### first : code = 종목코드(ex.'005930')
        ### second : start = 기준일자(ex.'20221102')
    ## return
        ### DataFrame
            #### open : 시작가
            #### high : 최고가
            #### low : 최저가
            #### close : 종가
            #### volumne : 거래량
    def get_total_data(self, code, start) :

        debug_log(__name__, f'OpenAPI에 종목번호({code})의 OHLCV 데이터 TR 요청')

    ## TR로 전달받은 데이터를 옮길 메모리 공간 준비
        self.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        
    ## TR 인자 설정 및 요청
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", start)
        self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    ## TR 데이터 옮기기
        while self.remained_data == True :
            self.set_input_value('종목코드', code)
            self.set_input_value("기준일자", start)
            self.set_input_value("수정주가구분", 1)
            self.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

    ## TR 조회 시 시간 간격 설정
        time.sleep(3.6)

    ## 데이터를 DataFrame 형태로 반환
        ### data가 비어있는 경우
        if len(self.ohlcv) == 0 :
            return []
        ### 장이 열리지 않은 날의 경우
        if self.ohlcv['date'] == '' :
            return []
        ### 장이 열린 날의 ohlcv 데이터를 DataFrame형태로 변환
        df = DataFrame(self.ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])#, index=self.ohlcv['date'])
        return df





# 모듈 테스트 코드
if __name__ == "__main__":
    app = QApplication(sys.argv)
    OpenAPI()