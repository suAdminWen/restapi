import tornado.ioloop
import tornado.web
from settings import settings
import api

urls = [
    (r"/api/article/?(\w+)?", api.Article),
    (r"/api/login", api.Login)
]


def make_app():
    return tornado.web.Application(urls, **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
