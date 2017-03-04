#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Just a test for verifying signup_routine."""
import sys
import unittest
# Make sure these folders point to the correct place
sys.path.insert(1, '../google-cloud-sdk/platform/google_appengine')
sys.path.insert(1, '../google-cloud-sdk/platform/google_appengine.ext')
sys.path.insert(
    1, '../google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
from google.appengine.api import memcache  # noqa
from google.appengine.ext import ndb  # noqa
from google.appengine.ext import testbed  # noqa
from verify_signup import (valid_email,  # noqa
                           valid_password,
                           valid_username,
                           verify_passwords_matches,
                           username_not_in_use
                          )
from Entities import UserEntity  # noqa


class TestModel(ndb.Model):
    """A model class used for testing."""
    number = ndb.IntegerProperty(default=42)
    text = ndb.StringProperty()


class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass


def GetEntityViaMemcache(entity_key):
    """Get entity from memcache if available, from datastore if not."""
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity


class DatastoreTestCase(unittest.TestCase):
    """Class for doing Entity-tests. (google-code)."""

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()


class UserEntityTest(DatastoreTestCase):
    """Test for User Account Entity."""


    def test_UserEntity_register(self):
        """UserEntity.register should create the useraccount, with correct data."""
        UserEntity.register(username='Jamie', password='password123').put()
        user = UserEntity.gql("WHERE username = 'Jamie'")[0]
        user2 = UserEntity.by_name('Jamie')
        user3 = UserEntity.by_name('Kelly')
        self.assertEqual(user.username, 'Jamie',
                         'gql-query should return a user.')
        self.assertEqual(user2.username, 'Jamie',
                         'UserEntity.by_name should return a user for existin user..')
        self.assertEqual(user3, None,
                         'UserEntity.by_name should return None if the user does not exist')
        self.assertNotEqual(user.password, 'password123',
                            'userpassword should be hashed, not stored as plain text')
        self.assertEqual(len(user.password), 60,
                         'userpassword should be hashed to 60 characters')


    def test_username_not_in_use(self):
        """Tests for checking if a username is already taken"""
        UserEntity.register(username='Jamie', password='password123').put()
        self.assertTrue(username_not_in_use('Jimmy'),
                        'username_not_in_use should return true if username not in use.')
        self.assertFalse(username_not_in_use('Jamie'),
                         'username_not_in_use should return false if username in use.')

    def test_UserEntity_register_same_username(self):
        UserEntity.register(username='Jamie', password='password123')
        UserEntity.register(username='Jamie', password='password123s')
        UserEntity.register(username='Jimmy', password='password123s')
        SameNameUsers = UserEntity.all().filter('username','Jamie')
        self.assertEqual(SameNameUsers.count(),1,
                         'UserEntity should only have unique usernames')



class UsernameTest(unittest.TestCase):
    """Testing username."""

    def test_valid_username_length_short(self):
        """valid_username should return false with input of less than 3 characters."""
        self.assertFalse(valid_username('jn'))

    def test_valid_username_length_ok(self):
        """valid_username should return True with input of between 3 and 20 characters."""
        self.assertTrue(valid_username('jon'))
        self.assertTrue(valid_username('abcdefghijklmnopqrst'))

    def test_valid_username_length_long(self):
        """valid_username should return False with input of more than 20 characters."""
        self.assertFalse(valid_username('abcdefghijklmnopqrstu'))

    def test_valid_non_valid_characters(self):
        """valid_username should return false with invalid characters"""
        self.assertFalse(valid_username('jonZå'))
        self.assertFalse(valid_username('sdf&'))
        self.assertFalse(valid_username('sdf&!'))

    def test_valid_valid_characters(self):
        """valid_username should return false with invalid characters"""
        self.assertTrue(valid_username('abcdefghijklmnopqrst'))
        self.assertTrue(valid_username('uvwxyz01234567890'))
        self.assertTrue(valid_username('john_doe'))
        self.assertTrue(valid_username('john-doe'))


class PasswordTest(unittest.TestCase):
    """Testing password."""

    def test_valid_password_length_short(self):
        """valid_password should return false with input of less than 3 characters."""
        self.assertFalse(valid_password('jn'))

    def test_valid_password_length_ok(self):
        """valid_password should return True with input of between 3 and 20 characters."""
        self.assertTrue(valid_password('jon'))

    def test_valid_password_length_long(self):
        """valid_password should return False with input of more than 20 characters."""
        self.assertFalse(valid_password('abcdefghijklmnopqrstu'))

    def test_valid_valid_characters(self):
        """valid_password should return false with invalid characters"""
        self.assertTrue(valid_password('abcdefghijklmnopqrst'))
        self.assertTrue(valid_password('uvwxyz01234567890'))
        self.assertTrue(valid_password('å˚!@$#*(&)'))
        self.assertTrue(valid_password('john-doe'))

    def test_verify_passwords_matches_true(self):
        """verify_passwords_matches should return true if passowords matches."""
        self.assertTrue(verify_passwords_matches(
            'password123', 'password123'))

    def test_verify_passwords_matches_false(self):
        """verify_passwords_matches should return false if passowords doesn't match."""
        self.assertFalse(verify_passwords_matches(
            'password123', 'password12'))


class EmailTest(unittest.TestCase):
    """Testing email."""
    # No more tests will be written here, no point as this is just an exercise

    def test_valid_valid_characters(self):
        """valid_email should return false with invalid characters"""
        self.assertTrue(valid_email('name@email.com'))
        self.assertTrue(valid_email('a@b.c'))
        self.assertTrue(valid_email('å@ø.cæm'))


if __name__ == '__main__':
    unittest.main()
