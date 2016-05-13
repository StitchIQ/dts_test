# coding=utf-8

from datetime import datetime

class Bug_Num_Generate(object):
    '''生成bug的id，格式为Bug + 日期时间（精确到秒） + 序列
       序列起始值为 100000
    '''
    num = 100000

    @staticmethod
    def bug_num():
        Bug_Num_Generate.num += 1
        return ''.join(['Bug', datetime.now().strftime("%Y%m%d%H%M"),
                        str(Bug_Num_Generate.num)])
