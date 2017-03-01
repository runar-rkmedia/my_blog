#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Just a test for verifying signup_routine."""
import unittest
from verify_signup import (valid_email, valid_password,
                           valid_username, verify_passwords_matches)


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
