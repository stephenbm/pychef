import time
from datetime import datetime, timedelta
from chef.api import ChefAPI
from chef.base import ChefObject

class Pushy(object):
    url = '/pushy/jobs'

    @classmethod
    def jobs(cls):
        api = api or ChefAPI.get_global()
        return api.api_request('GET', cls.url)

    @classmethod
    def start(cls, command, nodes, run_timeout=300, api=None):
        data = {
            'command': command,
            'nodes': nodes,
            'run_timeout': run_timeout
        }
        api = api or ChefAPI.get_global()
        return api.api_request('POST', url, data=data)
