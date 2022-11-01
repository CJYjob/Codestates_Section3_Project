ver = '# version 1.0.0'

import datetime
import os

debug_flag = 1

def debug_log(comment) :
    if debug_flag == 1 : print(f'Debug log({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {__file__}):{comment}')
