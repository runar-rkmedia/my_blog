"""checks for User-data. Part of myBlog."""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from Entities import UserEntity
import re
from Entities import UserEntity
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    """Check if a username is valid."""
    return bool(USER_RE.match(username))


def username_not_in_use(username):
    """Check that the username is not already in the database."""
    thisUser = UserEntity.by_name(username)
    return not bool(thisUser)

def valid_password(password):
    """Check that the password is valid."""
    return bool(PASS_RE.match(password))


def verify_passwords_matches(password1, password2):
    """Check that the passwords matches eachother."""
    return password1 == password2


def valid_email(email):
    """Check that the email-adress is valid."""
    return bool(EMAIL_RE.match(email))
