#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Just a test for verifying signup_routine."""
import sys
import unittest
import myExceptions
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
                           verify_passwords_matches
                          )
from Entities import CommentsEntity, VotesEntity, UserEntity, BlogEntity, blog_key  # noqa


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


class BlogEntityTest(DatastoreTestCase):
    """Test for blog entries."""

    def test_create_blog_entry(self):
        """."""
        james = UserEntity.register(username='james', password='pass')

        self.assertEqual(
            type(BlogEntity.create_blog_entry(
                parent=blog_key(),
                title='a',
                article='content',
                created_by=james)),
            BlogEntity, msg="'create_blog_entry' should return a BlogEntity")

    def test_create_blog_entry_with_existing_title(self):
        """BlogEntity.register should fail with a non-unique title."""
        james = UserEntity.register(username='james', password='pass')

        BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)
        self.assertRaises(
            myExceptions.NotUnique,
            BlogEntity.create_blog_entry,
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james,
        )

    def test_edit_blog_entry_with_existing_title(self):
        """edit_blog_post should fail if using a title from different post."""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)

        BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='b',
            article='content',
            created_by=james)

        self.assertRaises(
            myExceptions.NotUnique,
            a.edit_blog_entry,
            title='b',
            article='contents',
            created_by=james,
        )

    def test_delete_post_wrong_user(self):
        """delete_post should raise error if wrong user attempts to del it."""
        james = UserEntity.register(username='james', password='pass')
        kimmy = UserEntity.register(username='kimmy', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)

        self.assertRaises(
            myExceptions.EditOthersPosts,
            a.delete_post, kimmy)

    def test_delete_post(self):
        """delete_post should delete the post and its comments and votes."""
        james = UserEntity.register(username='james', password='pass')
        kimmy = UserEntity.register(username='kimmy', password='pass')
        dane = UserEntity.register(username='dane', password='pass')
        joe = UserEntity.register(username='joe', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)

        b = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='b',
            article='content',
            created_by=james)

        a.vote(voteBy=kimmy, voteType='up')
        a.vote(voteBy=dane, voteType='up')
        a.vote(voteBy=joe, voteType='down')
        b.vote(voteBy=kimmy, voteType='up')
        b.vote(voteBy=dane, voteType='up')
        b.vote(voteBy=joe, voteType='down')

        a.add_comment(commentBy=kimmy, comment='abc')
        a.add_comment(commentBy=dane, comment='abc')
        a.add_comment(commentBy=joe, comment='123')
        b.add_comment(commentBy=kimmy, comment='abc')
        b.add_comment(commentBy=dane, comment='abc')
        b.add_comment(commentBy=joe, comment='123')

        a.delete_post(james)
        votes = VotesEntity.all()
        for vote in votes:
            self.assertNotEqual(
                vote.voteOn.title,
                'a',
                msg="Votes of post 'a' should be deleted")
        comments = CommentsEntity.all()
        for comment in comments:
            self.assertNotEqual(
                comment.commentOn.title,
                'a',
                msg="Comments of post 'a' should be deleted")

        bloe_entries = BlogEntity.all()
        for blog_entity in bloe_entries:
            self.assertNotEqual(
                blog_entity.title,
                'a',
                msg="Post 'a' should be deleted")

    def test_edit_blog_entry_wrong_user(self):
        """edit_blog_post should fail if using a title from different post."""
        james = UserEntity.register(username='james', password='pass')
        jimmy = UserEntity.register(username='jimmy', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)

        self.assertRaises(
            myExceptions.EditOthersPosts,
            a.edit_blog_entry,
            title='a',
            article='contents',
            created_by=jimmy,
        )

    def test_edit_blog_entry_check_data(self):
        """edit_blog_post should fail if using a title from different post."""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a',
            article='content',
            created_by=james)

        a.edit_blog_entry(title='abc', article='123', created_by=james)
        self.assertEqual(a.title, 'abc', msg=None)
        self.assertEqual(a.article, '123', msg=None)

    def test_blog_get_by(self):
        """get_by_id_str and by_title should return the correct BlogEntity"""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a title',
            article='a content',
            created_by=james)

        a_id = str(a.key().id())

        self.assertEqual(
            BlogEntity.get_by_id_str(a_id).key().id(),
            a.key().id(),
            msg="'by_title' should return the 'a'-blog_entry")

        self.assertEqual(
            BlogEntity.by_title('a title').key().id(),
            a.key().id(),
            msg="'get_by_id_str' should return the 'a'-blog_entry")

    def test_blog_vote_on_own_post_fail(self):
        """user cannot vote on own post"""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a title',
            article='a content',
            created_by=james)

        self.assertRaises(myExceptions.VoteOnOwnPostNotAllowed,
                          a.vote, voteBy=james, voteType='up')

    def test_blog_add_comment(self):
        """.add_comment should return a CommentEnity if valid"""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a title',
            article='a content',
            created_by=james)

        self.assertEqual(
            type(a.add_comment(commentBy=james, comment='Awesome')),
            CommentsEntity)

    def test_blog_get_comments(self):
        """.get_comment should return a list of all CommentEnities on a post"""
        james = UserEntity.register(username='james', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a title',
            article='a content',
            created_by=james)

        a.add_comment(commentBy=james, comment='test')

        self.assertEqual(
            type(a.get_comments()[0]),
            CommentsEntity,
            msg="'get_comments should return a query of CommentsEntity'")

        self.assertEqual(
            a.get_comments().count(),
            1)

        self.assertEqual(
            a.get_comments()[0].comment, 'test')

    def test_blog_vote_on_others_post(self):
        """user should be able to vote on other posts"""
        james = UserEntity.register(username='james', password='pass')
        john = UserEntity.register(username='john', password='pass')
        jimbo = UserEntity.register(username='jimbo', password='pass')
        jake = UserEntity.register(username='jake', password='pass')
        jonas = UserEntity.register(username='jonas', password='pass')

        a = BlogEntity.create_blog_entry(
            parent=blog_key(),
            title='a title',
            article='a content',
            created_by=james)

        a.vote(voteBy=john, voteType='up')
        a.vote(voteBy=jimbo, voteType='down')
        a.vote(voteBy=jake, voteType='up')
        a.vote(voteBy=jonas, voteType='up')

        self.assertEqual(
            a.getVotes(),
            {'up': 3, 'down': 1},
            msg="'getvotes' should return a dict with keyword 'up' and 'down, here with values 3 and 1'")  # noqa

        self.assertEqual(
            a.getVotesFromUser(
                john), 'up', msg="'voting 'up' should set the vote to 'up'")

        a.vote(voteBy=john, voteType='up')
        self.assertEqual(
            a.getVotesFromUser(
                john),
            None,
            msg="'Voting 'up' twice should remove the vote")

        self.assertEqual(
            a.getVotesFromUser(
                jimbo),
            'down',
            msg="'voting 'down' should set the vote to 'down'")

        a.vote(voteBy=jimbo, voteType='down')
        self.assertEqual(
            a.getVotesFromUser(
                jimbo),
            None,
            msg="'Voting 'down' twice should remove the vote")


class UserEntityTest(DatastoreTestCase):
    """Test for User Account Entity."""

    def test_UserEntity_register(self):
        """UserEntity.register should create the account, with correct data."""
        UserEntity.register(username='Jamie', password='password123').put()
        user = UserEntity.gql("WHERE username = 'Jamie'")[0]
        user2 = UserEntity.by_name('Jamie')
        user3 = UserEntity.by_name('Kelly')
        self.assertEqual(user.username, 'Jamie',
                         'gql-query should return a user.')
        self.assertEqual(
            user2.username,
            'Jamie',
            'UserEntity.by_name should return a user for username.')
        self.assertEqual(
            user3,
            None,
            'UserEntity.by_name should return None if the user does not exist')
        self.assertNotEqual(
            user.password,
            'password123',
            'userpassword should be hashed, not stored as plain text')
        self.assertEqual(
            len(user.password),
            60,
            'userpassword should be hashed to 60 characters')

    def test_UserEntity_register_same_username(self):
        """
        UserEntity.register should return 'NotUnique'-exception
        if trying to register an account with the same username.
        """

        UserEntity.register(username='Jimmy', password='password123s')
        UserEntity.register(username='Jamie', password='password123')
        self.assertRaises(myExceptions.NotUnique,
                          UserEntity.register,
                          username='Jamie',
                          password='password123')


class UsernameTest(unittest.TestCase):
    """Testing username."""

    def test_valid_username_length_short(self):
        """valid_username should return false with input below 3 char."""
        self.assertFalse(valid_username('jn'))

    def test_valid_username_length_ok(self):
        """valid_username should return True with input whitin 3-20 char."""
        self.assertTrue(valid_username('jon'))
        self.assertTrue(valid_username('abcdefghijklmnopqrst'))

    def test_valid_username_length_long(self):
        """valid_username should return False with input over 20 chars."""
        self.assertFalse(valid_username('abcdefghijklmnopqrstu'))

    def test_valid_username_non_valid_characters(self):
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
        """valid_password should return false with input of below 3 chars."""
        self.assertFalse(valid_password('jn'))

    def test_valid_password_length_ok(self):
        """valid_password should return True with input whitin 3-20 chars."""
        self.assertTrue(valid_password('jon'))

    def test_valid_password_length_long(self):
        """valid_password should return False with input over 20 chars."""
        self.assertFalse(valid_password('abcdefghijklmnopqrstu'))

    def test_valid_valid_characters(self):
        """valid_password should return false with invalid characters"""
        self.assertTrue(valid_password('abcdefghijklmnopqrst'))
        self.assertTrue(valid_password('uvwxyz01234567890'))
        self.assertTrue(valid_password('å˚!@$#*(&)'))
        self.assertTrue(valid_password('john-doe'))

    def test_verify_passwords_matches_true(self):
        """verify_passwords_matches should return true if passwords matches."""
        self.assertTrue(verify_passwords_matches(
            'password123', 'password123'))

    def test_verify_passwords_matches_false(self):
        """verify_passwords_matches should return false if passwordmismatch."""
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
