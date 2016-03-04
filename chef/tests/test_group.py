import mock
import string
import random
from unittest2 import TestCase

from chef import Group
from chef.exceptions import ChefServerNotFoundError
from chef.tests import ChefTestCase


class UserTestCase(ChefTestCase):
    def setUp(self):
        super(UserTestCase, self).setUp()

    def random_ignore(self):
        valid_chars = string.ascii_lowercase + string.digits
        return ''.join(
            [random.choice(valid_chars) for _ in range(32)]
        )

    def test_populate(self):
        valid = self.random()
        invalid = self.random_ignore()
        group = Group(self.random())
        group._populate({'groups': [valid, invalid]})
        self.assertEqual(group.groups, [valid])

    def test_include(self):
        self.assertTrue(Group.include(self.random()))
        self.assertFalse(Group.include(self.random_ignore()))

    @mock.patch('chef.group.Group._check_api_version')
    def test_list(self, *args):
        fake_api = mock.MagicMock()
        valid = self.random()
        invalid = self.random_ignore()
        fake_api.__getitem__.return_value = {
            valid: '',
            invalid: ''
        }
        groups = Group.list(api=fake_api)
        self.assertEqual(groups.names, [valid])

    def test_add_member(self):
        group = Group(self.random())
        fake_entity = mock.MagicMock()
        fake_entity.exists = False
        self.assertRaises(ChefServerNotFoundError, group.add_member, fake_entity)
