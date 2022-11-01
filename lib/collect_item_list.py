ver = '# version 1.0.0'

# 내장 모듈 임포트

# 외장 모듈 임포트
import pandas as pd

# 제작 모듈 임포트
from lib.debug_log import debug_log

class stock_item_list() :
    
    def __init__(self) :
        debug_log(__name__, 'stock_item_list() 객체 생성')
        
        # 코스피 종목 가져오기
        self.get_item_kospi()

        # 코스닥 종목 가져오기
        self.get_item_kosdaq()

    def get_item_kospi(self) :
        debug_log(__name__, 'kospi 종목 리스트 받아오기 by get_item_kospi()')

        # web에서 kospi 정보 불러오기
        self.kospi_item_list = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=stockMkt', header=0)[0]
        
        # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
        # 6자리 만들고 앞에 0을 붙인다.
        self.kospi_item_list.종목코드 = self.kospi_item_list.종목코드.map('{:06d}'.format)

        # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
        self.kospi_item_list = self.kospi_item_list[['회사명', '종목코드']]

        # 한글로된 컬럼명을 영어로 바꿔준다.
        self.kospi_item_list = self.kospi_item_list.rename(columns={'회사명': 'code_name', '종목코드': 'code'})
        return self.kospi_item_list

    # 코스닥 종목 리스트를 가져오는 메서드
    def get_item_kosdaq(self):
        debug_log(__name__, 'kosdaq 종목 리스트 받아오기 by get_item_kosdaq()')

        # web에서 kosdaq 정보 불러오기
        self.kosdaq_item_list = \
        pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13&marketType=kosdaqMkt', header=0)[0]  
            
        # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
        # 6자리 만들고 앞에 0을 붙인다.
        self.kosdaq_item_list.종목코드 = self.kosdaq_item_list.종목코드.map('{:06d}'.format)

        # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
        self.kosdaq_item_list = self.kosdaq_item_list[['회사명', '종목코드']]

        # 한글로된 컬럼명을 영어로 바꿔준다.
        self.kosdaq_item_list = self.kosdaq_item_list.rename(columns={'회사명': 'code_name', '종목코드': 'code'})
        return self.kosdaq_item_list

# 모듈 테스트 코드
if __name__ == '__main__' :
    s = stock_item_list()
    print("코스피 종목 수: ", len(s.kospi_item_list))
    print(s.kospi_item_list)
    print(type(s.kospi_item_list))

    print("코스닥 종목 수: ", len(s.kosdaq_item_list))
    print(s.kosdaq_item_list)
    print(type(s.kospi_item_list))