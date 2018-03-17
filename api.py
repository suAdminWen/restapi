# -*- coding: utf-8 -*-
import json

import tornado.web
import datetime

from settings import db
from bson.objectid import ObjectId
from base import rtjson


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


class Article(ApiHandler):
    """
    1、完成了认证
    2、没有验证tornado的异步的牛逼之处
    """
    @tornado.web.asynchronous
    @tornado.web.authenticated
    def get(self, args=None):
        if args:
            try:
                article = db.article.find_one({"_id": ObjectId(args)})
                if not article:
                    raise Exception
            except Exception as err:
                print err
                article = {}
            self.finish(rtjson(article=article))
        else:
            article_list = list(db.article.find({}).sort('date', -1))
            self.finish(rtjson(article_list=article_list))

    @tornado.web.asynchronous
    @tornado.web.authenticated
    def put(self, args=None):
        article_id = args
        name = self.get_argument("name", None)
        content = self.get_argument("content", None)
        argument = {"name": name} if name else {}
        argument.update({"content": content}) if content else argument

        try:  # 这里对于id不合法的校验是不认真的，应该对传过来的参数进行校验
            if not content and not name:  # name 和 content 都不存在
                raise Exception
            db.article.update_one({"_id": ObjectId(article_id)},
                                  {'$set': argument}
                                  )
            article = db.article.find_one({"_id": ObjectId(article_id)})
        except Exception as err:
            print err
            article = {}
        return self.finish(rtjson(article=article))

    @tornado.web.asynchronous
    @tornado.web.authenticated
    def post(self, args=None):
        name = self.get_argument("name", None)
        content = self.get_argument("content", None)
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        try:
            if name and content:
                article_id = db.article.insert_one({
                    "name": name,
                    "date": date,
                    "content": content
                }).inserted_id
                article = db.article.find_one({"_id": ObjectId(article_id)})
                return self.finish(rtjson(article=article))
            else:
                return self.finish(rtjson(code=10001))
        except Exception as err:
            print err
            return self.finish(rtjson(code=10002))

    @tornado.web.asynchronous
    @tornado.web.authenticated
    def delete(self, args=None, **kwargs):
        if not args:
            return self.finish(rtjson(code=10004))
        try:
            article = db.article.find_one({"_id": ObjectId(args)})
            if article:
                db.article.delete_one({"_id": ObjectId(args)})
            else:
                raise Exception
            return self.finish(rtjson(article=article))
        except Exception as err:
            print err
            return self.finish(rtjson(code=10003))


class Login(ApiHandler):

    def post(self):
        name = self.get_argument("name", None)
        args = {"name": name}
        user = db.users.find_one(args)
        if not user:
            user = {
                "name": name,
                "password": "123456",
                "sex": "男"
            }
            user_id = db.users.insert_one(user).inserted_id
            user.update({"_id": str(user_id)})
        else:
            user_id = user["_id"] = str(user["_id"])

        token = self.create_signed_value('tid', str(user_id), version=2)
        user.update({"token": token})

        return self.finish(rtjson(**user))
