import json
import time
from eve.io.mongo import MongoJSONEncoder


def rtjson(code=1, **args):
    if code == 1:
        args['status'] = 1
        args['response_time'] = int(time.time())
    else:
        args['status'] = 0
        args['error_code'] = code
        # args['error_msg'] = errorDesc.get(code)
        args['response_time'] = int(time.time())

    return json.loads(json.dumps(args, cls=MongoJSONEncoder, sort_keys=True))
