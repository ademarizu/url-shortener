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

"""Tornado Application RequestHandler for URL's.
"""
from tornado.web import RequestHandler
from tornado.gen import coroutine
from tornado.gen import Future

import logging
LOG = logging.getLogger(__name__)


class URLHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        self.controller = None
        RequestHandler.__init__(self, application, request, **kwargs)

    def initialize(self, controller):
        LOG.debug("Initialized called - %s", controller)
        self.controller = controller

    @coroutine
    def get(self, id):
        url = yield self.get_url_by_id(id)
        if url:
            self.redirect(url, status=301)
        else:
            self.set_status(404, "Not found")

    def get_url_by_id(self, id, callback=None):
        url = self.controller.get_url_by_id(id)
        future = Future()
        future.set_result(url)
        return future

    def delete(self, id):
        self.controller.delete_url_by_id(id)