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
from urlshrtnr.dao.url import BaseUrlDao

class MockUrlDao(BaseUrlDao):

    def __init__(self):
        self.urls = {
            "abc": "http://www.uol.com.br",
            "def": "http://ademarizu.me"
        }

    def get_url_by_id(self, id):
        return self.urls.get(id, None)

    def delete_url_by_id(self, id):
        self.urls.pop(id)