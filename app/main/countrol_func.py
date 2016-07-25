# coding=utf-8
import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
import csv
import time
from datetime import datetime
from dateutil import tz

from flask import current_app

from ..models import Bugs

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


def utc2local(utc_st):
    """UTC时间转本地时间（+8:00）"""
    now_stamp = time.time()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    # print offset
    local_st = utc_st + offset
    return local_st

def output_csv_file(bug_list):
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + 'output.csv'

    with open(os.path.join(current_app.config['OUTPUT_FOLDER'], filename), 'wb') as csvfile:
        # 为了与windows兼容,不乱码,写入前,应该写入这几个字符: \xEF\xBB\xBF
        csvfile.write('\xEF\xBB\xBF')
        spamwriter = csv.writer(csvfile, dialect='excel')
        row = ("BugID",
                "提交人",
                "当前处理人",
                "产品名称",
                "产品版本",
                "软件版本",
                "软件特性",
                "问题级别",
                "问题定位人",
                "出现频率",
                "问题描述",
                "问题状态",
                "解决版本",
                "回归测试版本","创建时间","最后操作时间")
        spamwriter.writerow(row)

        for l in bug_list:
            res = Bugs.get_by_bug_id(l)
            row = (res.bug_id,
                   res.author.username,
                   res.bug_owner.username if res.bug_owner else None,
                   res.product_name,
                   res.product_version,
                   res.software_version,
                   res.version_features,
                   res.bug_level,
                   res.bug_insiders,
                   res.bug_show_times,
                   res.bug_title,
                   res.now_status.bug_status_descrit,
                   res.resolve_version,
                   res.regression_test_version,
                   utc2local(res.timestamp),
                   utc2local(res.bug_last_update)
                  )
            # print row
            spamwriter.writerow(row)
    return filename