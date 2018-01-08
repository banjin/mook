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
from elasticsearch import Elasticsearch, helpers
import logging
import re
import time
import traceback


def send_command(*commands):
    # 获取hive表中的数据
    cursor = hive.connect(host='13.21.184.153', port=10000).cursor()
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
    select_info = "select ip,scan_start_time,scan_end_time,provider_id,vuln_name,scan_type,level,risk_url,custom_name,harm_content,solution,threat_type,port from {table_name}".format(table_name=table_name)
    # result = send_command(select_info)
    r = re.compile(r'\s*select\s+(?P<fields>.*)\s+from\s+(?P<table>\S*)\s*')
    print select_info
    fields, table_name = re.match(r, select_info).groups()
    print fields
    print table_name
    table_name = table_name.strip()
    field_list = map(lambda x:x.strip(), fields.split(','))
    print "field_list",field_list
    doc_type, index = table_name, table_name
    field_list.extend(['_type', '_index'])
    result = send_command(select_info)
    write_doc_list(field_list, doc_type, index, result)

def write_doc_list(field_list, doc_type, index, result):

    es_hosts = ['http://42.159.206.8:9200/']
    es = Elasticsearch(
        hosts=es_hosts
    )

    start_time = time.time()
    doc_count = len(result)
    if doc_count > 0:
        make_mapping(doc_type, index, field_list, result[0])

    try:
        while len(result) > 0:
            if len(result) > 10000:
                doc_list = []
                for rs in result[0:10000]:
                    rs = list(rs)
                    rs.extend([doc_type, index])
                    doc_list.append(dict(zip(field_list, rs)))
                helpers.bulk(es, doc_list)
                del result[0:10000]
            else:
                doc_list = []
                for rs in result:
                    rs = list(rs)
                    rs.extend([doc_type, index])
                    doc_list.append(dict(zip(field_list, rs)))
                helpers.bulk(es, doc_list)
                result = []

        end_time = time.time()
    except Exception, e:
        traceback.print_exc()
        pass



def make_mapping(doc_type, index, field_list, data):
    properties = {}

    try:
        for i, value in enumerate(data):
            field = field_list[i]
            #logger.info("MAKE MAPPING TO  FIELD " + str(field))
            #logger.info("MAKE MAPPING TO  TYPE " + str(type(value)))
           # logger.info("MAKE MAPPING TO  VALUE " + str(value))

            if value is not None:
                if isinstance(value, unicode):
                    field_type = 'string'
                if isinstance(value, str):
                    field_type = 'string'
                if isinstance(value, int):
                    field_type = 'long'
                if isinstance(value, long):
                    field_type = 'long'
            else:
                field_type = 'string'

            #logger.info("MAKE MAPPING TO  FIELD TYPE  " + str(field_type))
            if field_type == 'string':
                properties[field] = {'type': field_type, "index": "not_analyzed"}
            else:
                properties[field] = {'type': field_type}

        mapping = {
                "mappings": {
                    doc_type: {
                      "properties": properties
                    }
                }
        }

        #logger.info("MAKE MAPPING TO  FIELD TYPE  " + str(mapping))

        es_hosts = ['http://42.19.26.8:9200/']
        es = Elasticsearch(hosts=es_hosts)
        es.indices.create(index=index, body=mapping)
        #logger.info("MAKE MAPPING END ")

    except Exception, e:
        #logger.info("MAKE MAPPING ERROR  " + e.__str__())
        traceback.print_exc()
        pass

if __name__=="__main__":
    get_all_fields('scan_20171228_11')
