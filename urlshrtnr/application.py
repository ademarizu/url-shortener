__author__ = 'ademarizu'
from tornado.web import Application
from urlshrtnr.handler.url import URLHandler
from urlshrtnr.controller.url import URLController


class UrlShrtnrApplication():

    def __init__(self):
        self.controllers = {"url": URLController()}

    def make_app(self):
        app = Application([
            (r"/url/(?P<id>[^\/]+)/?", URLHandler, dict(controller=self.controllers["url"]))
        ])
        return app