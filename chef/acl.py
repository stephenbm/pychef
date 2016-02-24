class _entity_map:
    _emap = {
        'User': 'actors',
        'Group': 'groups'
    }

    @classmethod
    def __getitem__(cls, key):
        return cls._emap[key.__name__]

    @classmethod
    def items(cls):
        return cls._emap.items()


class AclMixin(object):
    _acl_options = ['create', 'read', 'update', 'delete', 'grant']

    def _get_delta(self, permission, entities, current_access, add):
        updated = False
        if type(entities) is not list:
            entities = [entities]
        for etype, name in _entity_map.items():
            new_entities = filter(lambda x: type(x).__name__ == etype, entities)
            new_entities = [e.name for e in new_entities]
            if add and (set(current_access[name]) - set(new_entities)):
                current_access[name] = list(set(current_access[name] + new_entities))
                updated = True
            elif not add and (set(current_access[name]) & set(new_entities)):
                current_access[name] = list(set(current_access[name]) - set(new_entities))
        return updated

    @property
    def _acl_url(self):
        return '%s/_acl' % self.url

    def change(self, permissions, entities, api=None, add=True):
        if type(permissions) is not list:
            permissions = [permissions]
        api = api or self.api
        current_acl = self.get_acl(api=api)
        changes = []
        for permission in permissions:
            if self._get_delta(
                permission,
                entities,
                current_acl[permission],
                add
            ):
                changes.append(permission)
        return self.save_acl(current_acl, changes, api=api)

    def add(self, permissions, entities, api=None):
        return self.change(permissions, entities, api=api)

    def remove(self, permissions, entities, api=None):
        return self.change(permissions, entities, api=api, add=False)

    def get_acl(self, api=None):
        api = api or self.api
        return api.api_request('GET', self._acl_url)

    def save_acl(self, acl, changes, api=None):
        api = api or self.api
        for permission, entities in acl.items():
            result = api.api_request(
                'PUT',
                '%s/%s' % (self._acl_url, permission),
                data={permission: entities}
            )
        return acl
