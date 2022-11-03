# model 피클 가져오기

# import pickle

# import pandas as pd
# import FinanceDataReader as fdr

# model = None
# with open(r'C:\Users\raona\Desktop\codestates\Section3\s3prj\Codestates_Section3_Project\model.pkl','rb') as pickle_file:
#     model = pickle.load(pickle_file)

# # 종목 리스트 가져오기
# df_krx = fdr.StockListing('KRX')['Symbol']

# __init__.py

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        # if code in df_krx :
        #     df = fdr.DataReader('001250', '2018')
        #     df.loc[::-1].head(5)
        #     # X_test = 
        #     # y_pred = model.predict(X_test)

        #     return f'{}의 예상 가격은 ${int(y_pred)} 입니다.'
        # else :
        #     return "종목코드 ( %s ) 를 찾을 수 없습니다." % code
        return "종목코드 ( %s ) 를 입력하셨습니다. \n 예상 주가는 ( ) 입니다." % code
    else :
        return render_template('index.html')

