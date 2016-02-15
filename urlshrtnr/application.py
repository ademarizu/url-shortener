__author__ = 'ademarizu'
from tornado.web import Application
import tornado.options
from urlshrtnr.handler.url import URLHandler, URLStatsHandler
from urlshrtnr.controller.url import URLController
from urlshrtnr.handler.user import UserHandler, UserUrlHandler
from urlshrtnr.controller.user import UserController
from urlshrtnr.dao.url import RedisDao

from redis import StrictRedis
import logging
LOG = logging.getLogger(__name__)
tornado.options.parse_command_line()

class UrlShrtnrApplication():

    def __init__(self, domain, db_host, db_port, db_number, db_password=None):
        self.redis = StrictRedis(host=db_host, port=db_port, db=db_number, password=db_password)
        self.dao = RedisDao(self.redis)
        self.controllers = {"url": URLController(domain, self.dao),
                            "user": UserController(domain, self.dao)}
        self.domain = domain

    def make_app(self):
        LOG.info("Making app")
        app = Application([
            (r"/stats/?", URLStatsHandler, dict(controller=self.controllers["url"])),
            (r"/url/(?P<urlid>[^\/]+)/?", URLHandler, dict(controller=self.controllers["url"])),

            (r"/user/?", UserHandler, dict(controller=self.controllers["user"])),
            (r"/user/(?P<userid>[^\/]+)/?", UserHandler, dict(controller=self.controllers["user"])),
            (r"/user/(?P<userid>[^\/]+)/stats/?", UserHandler, dict(controller=self.controllers["user"])),
            (r"/users/(?P<userid>[^\/]+)/urls/?", UserUrlHandler, dict(controller=self.controllers["user"]))
        ])
        return app