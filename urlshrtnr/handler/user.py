__author__ = 'ademarizu'
#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Tornado Application RequestHandler for Users'.
"""
import simplejson
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import Future

import logging
LOG = logging.getLogger(__name__)


class UserHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.controller = None
	self.domain = application.domain
        RequestHandler.__init__(self, application, request, **kwargs)

    def initialize(self, controller):
        LOG.debug("Initialized called - %s", controller)
        self.controller = controller

    def post(self):
        body = self.request.body
        LOG.debug("[post] - body: %s", type(body))
        user_dict = simplejson.loads(body)
        self.controller.add_user(user_dict)

    def delete(self, userid):
        self.controller.delete_user_by_userid(userid)

    @coroutine
    def get(self, userid):
	LOG.debug("[get] - Get called with userid (%s)")
        stats = yield self.get_user_stats_by_id(userid)
        if stats:
            self.add_header("Content-Type", "application/json")
            self.write(simplejson.dumps(stats))
        else:
            self.set_status(404, "Not found")

    def get_user_stats_by_id(self, userid):
        future = Future()
        stats = self.controller.get_user_stats_by_id(userid)
        future.set_result(stats)
        return future

class UserUrlHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.controller = None
        self.domain = application.domain
        RequestHandler.__init__(self, application, request, **kwargs)

    def initialize(self, controller):
        LOG.debug("Initialized called - %s", controller)
        self.controller = controller

    @coroutine
    def post(self, userid):
        body = self.request.body
        LOG.debug("[post] - body: %s", type(body))
        url_dict = simplejson.loads(body)
        result = yield self.add_user_url(userid, url_dict)
        self.write(result)

    def add_user_url(self, userid, url_dict):
        future = Future()
        future.set_result(self.controller.add_user_url(userid, url_dict))
        return future



