__author__ = 'ademarizu'
from tornado.web import Application
from urlshrtnr.handler.url import URLHandler
from urlshrtnr.controller.url import URLController
from urlshrtnr.handler.user import UserHandler
from urlshrtnr.controller.user import UserController
from urlshrtnr.dao.url import RedisUrlDao

from redis import StrictRedis


class UrlShrtnrApplication():

    def __init__(self):
        self.redis = StrictRedis(host="192.168.59.103", port=6379, db=0, password=None)
        self.dao = RedisUrlDao(self.redis)
        self.controllers = {"url": URLController(self.dao),
                            "user": UserController(self.dao)}

    def make_app(self):
        app = Application([
            (r"/url/(?P<id>[^\/]+)/?", URLHandler, dict(controller=self.controllers["url"])),
            (r"/user/?", UserHandler, dict(controller=self.controllers["user"])),
            (r"/user/(?P<userid>[^\/]+)/?", UserHandler, dict(controller=self.controllers["user"])),
            (r"/user/(?P<userid>[^\/]+)/stats/?", UserHandler, dict(controller=self.controllers["user"]))
        ])
        return app