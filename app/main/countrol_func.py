# coding=utf-8
import os
import csv
from datetime import datetime

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

def output_csv_file(bug_list):
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + 'output.csv'

    with open(os.path.join(current_app.config['OUTPUT_FOLDER'], filename), 'wb') as csvfile:
        # 为了与windows兼容,不乱码,写入前,应该写入这几个字符: \xEF\xBB\xBF
        csvfile.write('\xEF\xBB\xBF')
        spamwriter = csv.writer(csvfile, dialect='excel')
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
                   res.system_view,
                   res.bug_show_times,
                   res.bug_title,
                   res.now_status.bug_status_descrit,
                   res.resolve_version,
                   res.regression_test_version)
            # print row
            spamwriter.writerow(row)
    return filename