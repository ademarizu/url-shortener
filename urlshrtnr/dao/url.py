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

    def get_url_by_id(self, id):
        return self.redis.get(self.get_key(id))

    def delete_url_by_id(self, id):
        self.redis.delete(self.get_key(id))

    def get_key(self, id):
        """
        Generates a proper Redis key for URLS
        :param id: url's id.
        :return: A string like 'URL:<id>'.
        """
        return "URL:%s" %id