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

"""Controller for url.
"""
import logging
LOG = logging.getLogger(__name__)

class URLController():

    def __init__(self, url_dao):
        self.url_dao = url_dao

    def get_url_by_urlid(self, urlid):
        """
        Retrieves an url by its id.
        :param urlid: url's id.
        :return: url if found, None otherwise
        """
        LOG.debug("[get_url_by_urlid] - Getting url by id: %s", urlid)
        self.url_dao.increase_url_stats_by_urlid(urlid)
        return self.url_dao.get_url_by_urlid(urlid)

    def get_total_stats(self):
        """
        Retrieves urls stats
        :return: dict object with urls stats
        """
        stats = {
            "hits": self.url_dao.get_total_of_hits(),
            "urlCount": self.url_dao.get_urls_count(),
            "topUrls": self.url_dao.get_top_urls()
        }
        return stats

    def delete_url_by_urlid(self, urlid):
        self.url_dao.delete_url_by_urlid(urlid)