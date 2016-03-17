import time
import datetime
from chef.api import ChefAPI
from chef.base import ChefObject

class Report(object):

    @classmethod
    def _unix_stamp(cls, dt):
        return int(time.mktime(dt.timetuple()))

    @classmethod
    def fetch(cls, node=None, start_time=None, end_time=None, status=None, rows=10, api=None):
        search = node and 'nodes/%s' % node or 'org'
        api = api or ChefAPI.get_global()
        full_url = '/reports/%s/runs?' % (search)
        if start_time:
            full_url = full_url + ('from=%s' % cls._unix_stamp(start_time))
        if end_time:
            full_url = full_url + ('&until=%s' % cls._unix_stamp(end_time))
        if rows:
            full_url = full_url + ('&rows=%s' % rows)
        return api.api_request('GET',
            full_url,
            headers={'X-Ops-Reporting-Protocol-Version': '0.1.0'}
        )
