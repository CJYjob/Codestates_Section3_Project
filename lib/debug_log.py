ver = '# version 1.0.0'

import datetime

import inspect

debug_flag = 1

# print debugging comment
def debug_log(filename, comment) :
    if debug_flag == 1 : print(f'Debug log({datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, {filename}):{comment}')
