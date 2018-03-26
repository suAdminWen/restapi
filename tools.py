# coding=utf-8
import json
import time
from eve.io.mongo import MongoJSONEncoder

errorDesc = {10001: "error 10001",
             10002: "error 10002",
             10003: "error 10003",
             10004: "error 10004"}


def rtjson(code=1, **args):
    if code == 1:
        args['status'] = 1
        args['response_time'] = int(time.time())
    else:
        args['status'] = 0
        args['error_code'] = code
        args['error_msg'] = errorDesc.get(code)
        args['response_time'] = int(time.time())

    return json.loads(json.dumps(args, cls=MongoJSONEncoder, sort_keys=True))


def mongoPager(docs, pagenum=1, pagesize=20):
    """
    这里封装的分页处理
    :param docs:
    :param pagenum:  获取的页数
    :param pagesize:  每页的大小
    :return:
    """
    total = docs.count()
    page_total = int((total / pagesize + 1) if total % pagesize != 0 else (total / pagesize))
    pager = {
        'pagesize': pagesize,
        'pagenum': pagenum,  # 请求页码
        'total': total,  # 记录总数
        'page_total': page_total,  # 总页数
        'start': (pagenum - 1) * pagesize,
        'end': pagenum * pagesize
    }
    doc_list = list(docs.skip(pager['start']).limit(pager['pagesize']))
    return doc_list, pager
