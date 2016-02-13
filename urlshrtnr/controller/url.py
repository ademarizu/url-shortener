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

    def get_url_by_id(self, id):
        """
        Retrieves an url by its id.
        :param id: url's id.
        :return: url if found, None otherwise
        """
        return self.url_dao.get_url_by_id(id)
