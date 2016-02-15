from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from urlshrtnr.application import UrlShrtnrApplication

# Simple main to initialize service
if __name__ == "__main__":

    server = HTTPServer(UrlShrtnrApplication().make_app())
    server.bind(8888)
    server.start(0)  # Forks multiple sub-processes
    IOLoop.current().start()
