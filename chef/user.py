import re
import six
from chef.api import ChefAPI
from chef.base import ChefObject, ChefQuery

class User(ChefObject):
    """A User group object."""

    url = '/users'
    attributes = {
        'email': str,
        'first_name': str,
        'middle_name': str,
        'last_name': str,
        'display_name': str,
        'password': str,
        'create_key': bool
    }

    def __init__(self, name, api=None, skip_load=False):
        api = User._user_api(api=api)
        super(User, self).__init__(name, api=api, skip_load=skip_load)

    @classmethod
    def _user_api(cls, api=None):
        api = api or ChefAPI.get_global()
        url = '/'.join(api.url.split('/')[:3])
        api_args = (url, api.key, api.client)
        api_kwargs = {
            'version': api.version,
            'headers': api.headers,
            'ssl_verify': api.ssl_verify
        }
        return ChefAPI(*api_args, **api_kwargs)

    @classmethod
    def list(cls, api=None):
        return super(User, cls).list(api=cls._user_api(api=api))

    @classmethod
    def create(cls, name, api=None, **kwargs):
        return super(User, cls).create(name, api=cls._user_api(api=api), **kwargs)

    def save(self, api=None):
        return super(User, self).save(api=User._user_api(api=api))

    def delete(self, api=None):
        return super(User, self).delete(api=User._user_api(api=api))

    def to_dict(self):
        d = super(User, self).to_dict()
        d['username'] = d['name']
        del d['name']
        del d['json_class']
        del d['chef_type']
        return d
