# coding=utf-8
import json
import tornado.web


class ApiHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_argument(self, name, default=None, strip=True):
        if self.request.method != "GET":
            if 'application/json' in str(self.request.headers.get('Content-Type')) and self.request.body and self.request.body != '{}' \
                    and self.request.body.startswith('{'):
                obj = json.loads(self.request.body)
                return obj.get(name, default)
            elif 'application/x-www-form-urlencoded' in str(self.request.headers.get('Content-Type')) \
                    and self.request.body and self.request.body != '{}' \
                    and self.request.body.startswith('{'):
                obj = json.loads(self.request.body)
                return obj.get(name, default)
        return self._get_argument(name, default, self.request.arguments, strip)

    def options(self):
        self.__set_response_header()

    # 这里的意思是在返回时附带允许请求的http response 头
    def __set_response_header(self):
        self.set_header('content-type', 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods',
                        'POST, GET, OPTIONS, HEAD')
