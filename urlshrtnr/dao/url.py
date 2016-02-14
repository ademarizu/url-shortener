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
import logging
LOG = logging.getLogger(__name__)


class BaseUrlDao():

    def get_url_by_id(self, id):
        """
        Retrieves an url by its id.
        :param id: url's id.
        :return: url if found, None otherwise
        """
        pass

    def delete_url_by_id(self, id):
        """
        Deletes an url by its id.
        :param id: url's id.
        """
        pass


class RedisUrlDao(BaseUrlDao):

    def __init__(self, redis):
        """
        Constructor method that receives a StrictRedis instance
        :param redis: StrictRedis instance
        """
        self.redis = redis

    def add_user(self, userid):
        self.redis.set("USER:%s" %userid, userid)

    def add_user_url(self, userid, url):
        self.redis.zadd("URL")

    def get_url_by_urlid(self, urlid):
        return self.redis.get(self.get_url_key(urlid))

    def increase_url_stats_by_urlid(self, urlid):
        LOG.debug("[increase_url_stats_by_urlid] - Increasing url stats for %s", urlid)
        userid = self.get_userid_by_url_urlid(urlid)
        LOG.debug("[increase_url_stats_by_urlid] - url's user is %s", userid)

        self.increase_user_total_hits(userid)
        self.increase_user_urls_hits_list(userid, urlid)

        self.redis.incrby("URL:TOTAL_HITS")
        self.redis.zincrby("URL:TOP_HITS", "URL:%s" %urlid)
        stats = {
            "hits": "URL:TOTAL_HITS",
            "urlCount": "",
            "topUrls": [],
        }

    def increase_user_urls_hits_list(self, userid, urlid, hits=1):
        """
        Increases total hits for a user's url list
        :param userid:
        :param urlid:
        """
        self.redis.zincrby("USER:%s:URLS" %userid, "URL:%s" %urlid, hits)

    def increase_user_total_hits(self, userid):
        """
        Increases total hits for user
        :param userid: user id
        """
        self.redis.incrby("USER:%s:TOTAL_HITS" %userid)


    def get_userid_by_url_urlid(self, urlid):
        """
        Retrieves user by a given url id
        :param urlid: url id
        :return: userid
        """
        url_user_key = "URL:%s:USER" %id
        return self.redis.get(url_user_key)

    def get_user_total_hits_by_userid(self, userid):
        total = self.redis.get("USER:%s:TOTAL_HITS" %userid)
        return total if total else 0

    def get_user_number_of_urls_by_userid(self, userid):
        """
        Retrieves number of user urls
        :param userid: user id
        :return: number of urls
        """
        return self.redis.zcount("USER:%s:URLS" %userid, 0, -1)

    def get_user_top_urls_by_userid(self, userid, count=10):
        urls = self.redis.zrevrange("USER:%s:URLS" %userid, 0, (count - 1))
        return urls

    def delete_url_by_urlid(self, urlid):
        self.redis.delete(self.get_url_key(urlid))

    def get_url_key(self, urlid):
        """
        Generates a proper Redis key for URLS
        :param id: url's id.
        :return: A string like 'URL:<id>'.
        """
        return "URL:%s" %id
