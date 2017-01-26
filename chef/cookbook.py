import requests

from chef.api import ChefAPI
from chef.base import ChefObject
from chef.exceptions import ChefError, ChefServerNotFoundError
from chef.acl import AclMixin


class Cookbook(ChefObject, AclMixin):
    """A Chef cookbook object."""

    url = '/cookbooks'
    attributes = {
        'cookbook_name': str,
        'root_files': list
    }

    def __init__(self, name, version='_latest', api=None, skip_load=False):
        super(Cookbook, self).__init__(name + '/' + version, api=api, skip_load=skip_load)

    def file_url(self, path):
        for root_file in self.root_files:
            if root_file['name'] == path:
                return root_file['url']

    def file_content(self, path):
        url = self.file_url(path)
        if not url:
            raise ChefServerNotFoundError('%s node found in %s' % (path, self.cookbook_name))
        result = requests.get(url, verify=False)
        if result.status_code == 200:
            return result.text
        raise ChefError()
