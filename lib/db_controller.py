ver = '# version 1.0.0'

# 모듈 임포트
    ## 내장 모듈 임포트

    ## 외장 모듈 임포트
import pymysql
from sqlalchemy import create_engine

    ## 제작 모듈 임포트
from lib.debug_log import debug_log


# declare db_controller class
class db_controller:
    def __init__(self):
        debug_log(__name__, "db_controller.__init__()")
        self.engine = None

    def db_setting(self, db_name, db_id, db_passwd, db_ip, db_port):
        debug_log(__name__, "db_setting()")
        # mysql 데이터베이스랑 연동하는 방식.
        self.engine = create_engine("mysql+mysqldb://" + db_id + ":" + db_passwd + "@"
                                        + db_ip + ":" + db_port + "/" + db_name, encoding='utf-8')
