import re
import six
from chef.api import ChefAPI
from chef.base import ChefObject, ChefQuery
from chef.exceptions import ChefServerNotFoundError
from chef.user import User
from chef.acl import AclMixin


class Group(ChefObject, AclMixin):
    """A Chef group object."""

    url = '/groups'
    attributes = {
        'users': list,
        'groups': list,
        'clients': list,
        'orgname': str,
        'groupname': str
    }

    def _populate(self, data):
        super(Group, self)._populate(data)
        setattr(self, 'groups', filter(Group.include, getattr(self, 'groups')))

    @classmethod
    def include(cls, name):
        return not re.match(r'^[a-z0-9]{32}$', name)

    @classmethod
    def list(cls, api=None):
        """Return a :class:`ChefQuery` with the available objects of this type.
        """
        api = api or ChefAPI.get_global()
        cls._check_api_version(api)
        names = [
            name for name, url in six.iteritems(api[cls.url])
            if Group.include(name)
        ]
        return ChefQuery(cls, names, api)

    def add_member(self, member):
        mtype = type(member).__name__
        mlist = getattr(self, '%ss' % mtype.lower())
        if not member.exists:
            raise ChefServerNotFoundError('%s %s does not exist' % (
                mtype, member.name
            ))
        if member.name in mlist:
            return
        mlist.append(member.name)
        self.save()
    add_user = add_client = add_group = add_member

    def remove_member(self, member):
        mtype = type(member).__name__
        mlist = getattr(self, '%ss' % mtype.lower())
        if not member.exists:
            raise ChefServerNotFoundError('%s %s does not exist' % (
                mtype, member.name
            ))
        if member.name not in mlist:
            return
        mlist.remove(member.name)
        self.save()
    remove_user = remove_client = remove_group = remove_member

    def to_dict(self):
        d = super(Group, self).to_dict()
        d['actors'] = {}
        d['groupname'] = d['groupname'] or d['name']
        for atype in ['users', 'groups', 'clients']:
            d['actors'][atype] = getattr(self, atype)
            del d[atype]
        return d
