import mock
from unittest2 import TestCase

import re
from chef import User
from chef.api import ChefAPI
from chef.tests import ChefTestCase


class UserTestCase(ChefTestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.api = ChefAPI.get_global()
        self.user_api = User._user_api(api=self.api)
        User._user_api = mock.MagicMock(return_value=self.user_api)

    def test_user_api(self):
        self.assertTrue(bool(re.match(r'^https?://[^/]+/?$', self.user_api.url)))

    @mock.patch('chef.base.ChefObject.list')
    def test_list(self, base_list):
        users = User.list()
        base_list.assert_called_with(api=self.user_api)

    @mock.patch('chef.api.ChefAPI.request')
    @mock.patch('chef.base.ChefObject.create')
    def test_create(self, base_create, *args):
        name = self.random()
        user = User.create(name)
        user.name = name
        base_create.assert_called_with(name, api=self.user_api)
        self.assertEqual(user.name, name)

    @mock.patch('chef.base.ChefObject.__init__')
    @mock.patch('chef.base.ChefObject.save')
    def test_save(self, base_save, *args):
        user = User(self.random())
        user.save()
        base_save.assert_called_with(api=self.user_api)

    @mock.patch('chef.base.ChefObject.__init__')
    @mock.patch('chef.base.ChefObject.delete')
    def test_delete(self, base_delete, *args):
        user = User(self.random())
        user.delete()
        base_delete.assert_called_with(api=self.user_api)
