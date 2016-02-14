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


class URLController():

    def __init__(self, url_dao):
        self.url_dao = url_dao

    def get_url_by_urlid(self, id):
        """
        Retrieves an url by its id.
        :param id: url's id.
        :return: url if found, None otherwise
        """
        self.url_dao.increase_url_stats_by_urlid(id)
        return self.url_dao.get_url_by_urlid(id)

    def get_total_stats(self):
        """
        Retrieves urls stats
        :return: dict object with urls stats
        """
        stats = {
            "hits": self.url_dao.get_total_of_hits(),
            "urlCount": self.user_dao.get_urls_count(),
            "topUrls": self.user_dao.get_user_top_urls_by_userid(userid),
        }