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

"""Controller for user.
"""

class UserController():

    def __init__(self, user_dao):
        self.user_dao = user_dao

    def add_user(self, user_dict):
        userid = user_dict.get("id", None)
        self.user_dao.add_user(userid)

    def add_user_url(self, userid, url_dict):
        url = url_dict["url"]
        urlid = self.user_dao.add_user_url(userid, url)

        response = {
            "id": urlid,
            "hits": self.user_dao.get_hits_of_url_by_urlid(urlid),
            "url": url,
            "shortUrl": "url/%s" %urlid
        }
        return response

    def delete_user_by_userid(self, userid):
        self.user_dao.delete_user_by_userid(userid)

    def get_user_stats_by_id(self, userid):
        stats = {
            "hits": self.user_dao.get_user_total_hits_by_userid(userid),
            "urlCount": self.user_dao.get_user_number_of_urls_by_userid(userid),
            "topUrls": self.user_dao.get_user_top_urls_by_userid(userid),
        }
        return stats