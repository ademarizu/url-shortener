import argparse
import logging

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from urlshrtnr.application import UrlShrtnrApplication

class UrlShrtnrApplicationCli():

    def __init__(self):
        pass

    def run(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--domain", dest="domain", help="Domain for urls", required=True)
        parser.add_argument("-p", "--serverport", dest="port", help="Server port", required=False, default=8888)
        parser.add_argument("-a", "--host", dest="db_host", help="DB Host", required=True)
        parser.add_argument("-r", "--dbport", dest="db_port", help="DB Port", required=False, default=6379)
        parser.add_argument("-n", "--number", dest="db_number", help="DB Number", required=False, default=0)
        parser.add_argument("-w", "--password", dest="db_password", help="DB Password", required=False, default=None)

        values = parser.parse_args(args)
        self.init(values.domain, values.port, values.db_host, values.db_port, values.db_number, values.db_password)

    def init(self, domain, port, db_host, db_port, db_number, db_password):
        shrtnr_app = UrlShrtnrApplication(domain, db_host, db_port, db_number, db_password)
        server = HTTPServer(shrtnr_app.make_app())
        server.bind(port)
        server.start(0)  # Forks multiple sub-processes
        IOLoop.current().start()


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    UrlShrtnrApplicationCli().run(sys.argv[1:])
