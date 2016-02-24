from chef.base import ChefObject
from chef.acl import AclMixin

class Role(ChefObject, AclMixin):
    """A Chef role object."""

    url = '/roles'
    attributes = {
        'description': str,
        'run_list': list,
        'default_attributes': dict,
        'override_attributes': dict,
        'env_run_lists': dict
    }
