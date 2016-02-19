import re
import six
from chef.api import ChefAPI
from chef.base import ChefObject, ChefQuery

class Group(ChefObject):
    """A Chef group object."""

    url = '/groups'

    @classmethod
    def list(cls, api=None):
        """Return a :class:`ChefQuery` with the available objects of this type.
        """
        api = api or ChefAPI.get_global()
        cls._check_api_version(api)
        names = [
            name for name, url in six.iteritems(api[cls.url])
            if not re.match(r'^[a-z0-9]{32}$', name)
        ]
        return ChefQuery(cls, names, api)


    def to_dict(self):
        d = super(Group, self).to_dict()
        d['groupname'] = d['name']
        del d['name']
        return d
