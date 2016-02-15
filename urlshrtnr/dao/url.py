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

class RedisDao():

    def __init__(self, redis):
        """
        Constructor method that receives a StrictRedis instance
        :param redis: StrictRedis instance
        """
        self.redis = redis

    def add_user(self, userid):
        self.redis.set(self.get_user_key(userid), userid)

    def add_user_url(self, userid, url):
        initial_hit_score = 0
        urlid = self.redis.incrby("URL:INDEX")
        url_key = self.get_url_key(urlid)
        self.redis.set(url_key, url)
        self.redis.set(self.get_url_user_key(urlid), userid)
        self.redis.zadd(self.get_user_urls_key(userid), initial_hit_score,  url_key)
        self.redis.zadd(self.get_top_urls_key(), initial_hit_score,  url_key)

        return urlid

    def get_url_by_urlid(self, urlid):
        LOG.info("[get_url_by_urlid] - Getting url by urlid %s", urlid)
        return self.redis.get(self.get_url_key(urlid))

    def increase_url_stats_by_urlid(self, urlid):
        LOG.debug("[increase_url_stats_by_urlid] - Increasing url stats for %s", urlid)

        userid = self.get_userid_by_url_urlid(urlid)
        LOG.debug("[increase_url_stats_by_urlid] - url's user is %s", userid)

        self.increase_user_total_hits(userid)
        self.increase_user_urls_hits_list(userid, urlid)

        self.redis.incrby(self.get_url_hits_key(urlid))
        self.redis.incrby(self.get_urls_total_hits_key())
        self.redis.zincrby(self.get_top_urls_key(), "URL:%s" %urlid)

    def increase_user_urls_hits_list(self, userid, urlid):
        """
        Increases total hits for a user's url list
        :param userid:
        :param urlid:
        """
        self.redis.zincrby(self.get_user_urls_key(userid), "URL:%s" %urlid)

    def get_user_total_hits_key(self, userid):
        return "USER:%s:TOTAL_HITS" % userid

    def increase_user_total_hits(self, userid):
        LOG.debug("[increase_user_total_hits] - Increasing user (%s) total hits", userid)
        """
        Increases total hits for user
        :param userid: user id
        """
        self.redis.incrby(self.get_user_total_hits_key(userid))


    def get_userid_by_url_urlid(self, urlid):
        """
        Retrieves user by a given url id
        :param urlid: url id
        :return: userid
        """
        LOG.debug("Retrieving user for url's id: %s", urlid)
        url_user_key = self.get_url_user_key(urlid)
        return self.redis.get(url_user_key)

    def get_user_total_hits_by_userid(self, userid):
        total = self.redis.get(self.get_user_total_hits_key(userid))
        return total if total else 0

    def get_hits_of_url_by_urlid(self, urlid):
        hits = self.redis.get(self.get_url_hits_key(urlid))
        return hits if hits else 0

    def get_user_number_of_urls_by_userid(self, userid):
        """
        Retrieves number of user urls
        :param userid: user id
        :return: number of urls
        """
        return self.redis.zcard(self.get_user_urls_key(userid))

    def get_urls_count(self):
        total = self.redis.zcard(self.get_top_urls_key())
        return total if total else 0

    def get_total_of_hits(self):
        total = self.redis.get(self.get_urls_total_hits_key())
        return total if total else 0

    def get_top_urls(self, count=10):
        urls = self.redis.zrevrange(self.get_top_urls_key(), 0, (count - 1))
        return urls

    def get_user_top_urls_by_userid(self, userid, count=10):
        urls = self.redis.zrevrange(self.get_user_urls_key(userid), 0, (count - 1))
        return urls

    def delete_user_by_userid(self, userid):
        """
        Deletes user and all its urls references.
        :param userid: user's id.
        """
        #Deleting all user's urls
        for urlid in self.redis.zrevrange(self.get_user_urls_key(userid), 0, -1):
            self.delete_url_by_urlid(urlid.split(":")[1])

        #Deleting user's hits
        self.redis.delete(self.get_user_total_hits_key(userid))

        #Deleting user's urls list
        self.redis.delete(self.get_user_urls_key(userid))

        #Deleting user reference
        self.redis.delete(self.get_user_key(userid))

    def delete_url_by_urlid(self, urlid):
        LOG.debug("Deleting url %s", urlid)
        """
        Deletes all redis references of URL given its id.
        :param urlid: url's id.
        """
        #First, retrieving url's hits count and user
        url_hits = int(self.get_hits_of_url_by_urlid(urlid))
        url_user = self.get_userid_by_url_urlid(urlid)

        #Deleting url's hit count reference
        self.redis.delete(self.get_url_hits_key(urlid))

        #Deleting url's user reference
        self.redis.delete(self.get_url_user_key(urlid))

        #Deleting url's reference
        self.redis.delete(self.get_url_key(urlid))

        #Deleting url from urls list
        self.redis.zrem(self.get_top_urls_key(), self.get_url_key(urlid))

        #Deleting url from user's urls list
        self.redis.zrem(self.get_user_urls_key(url_user), self.get_url_key(urlid))

        #Decreasing urls total hits
        self.redis.incrby(self.get_urls_total_hits_key(), -url_hits)

        #Decreasing user total hits
        self.redis.incrby(self.get_user_total_hits_key(url_user), -url_hits)

    def get_url_key(self, urlid):
        """
        Generates a proper Redis key for URLS
        :param id: url's id.
        :return: A string like 'URL:<id>'.
        """
        return "URL:%s" %urlid

    def get_url_user_key(self, urlid):
        """
        Generates a proper Redis key for URL's user
        :param id: url's id.
        :return: A string like 'URL:<id>:USER'.
        """
        return "URL:%s:USER" % urlid

    def get_user_urls_key(self, userid):
        """
        Generates a proper Redis key for User Urls List
        :param userid: user.
        :return: A string like 'USER:<id>:URLS'.
        """
        return "USER:%s:URLS" % userid

    def get_url_hits_key(self, urlid):
        """
        Generates a proper Redis key for URL's hits
        :param id: url's id.
        :return: A string like 'URL:<id>:HITS'.
        """
        return "URL:%s:HITS" % urlid

    def get_urls_total_hits_key(self):
        return "URL:TOTAL_HITS"

    def get_top_urls_key(self):
        return "URL:TOP_HITS"

    def get_user_key(self, userid):
        return "USER:%s" % userid




