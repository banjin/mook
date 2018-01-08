# coding:utf8
# pip install pyhive
# pip install thrift
#sasl==0.2.1
#thrift_sasl==0.2.1
#hive-thrift-py==0.0.1
#elasticsearch

from pyhive import hive
from TCLIService.ttypes import TOperationState
import datetime
#from elasticsearch import Elasticsearch, helpers
import logging
import re
import time
import traceback


def send_command(*commands):
    # 获取hive表中的数据
    cursor = hive.connect(host='139.219.184.153', port=10000).cursor()
    for cd in commands:
        cursor.execute(cd, async=False)

    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE, 5):
        logs = cursor.fetch_logs()
        for message in logs:
            print message
        # If needed, an asynchronous query can be cancelled at any time with:
        # cursor.cancel()
        status = cursor.poll().operationState

    return cursor.fetchall()


def get_all_fields(table_name):
    # 查询出字段名和表名, 用于存储在es中的数据
    select_info = """select ip,scan_start_time,scan_end_time,provider_id ,vuln_name ,scan_type ,level ,risk_url ,custom_name ,harm_content ,solution ,threat_type ,port from {table_name};""".format(table_name=table_name)
    # result = send_command(select_info)
    r = re.compile(r'\s*select\s+(?P<fields>.*)\s+from\s+(?P<table>\S*)\s*')
    print select_info
    fields, table_name = re.match(r, select_info).groups()
    print fields
    print table_name
    table_name = table_name.strip()
    field_list = map(lambda x:x.strip(), fields.split(','))
    doc_type, index = table_name, table_name

if __name__ == "__main__":
    #data = send_command("select * from scan_20171228_11 limit 10")
    #print data
    get_all_fields('scan_20171228_11')
