"""checks for User-data. Part of myBlog."""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def valid_username(username):
    """Check if a username is valid."""
    user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return bool(user_re.match(username))


def valid_password(password):
    """Check that the password is valid."""
    pass_re = re.compile(r"^.{3,20}$")
    return bool(pass_re.match(password))


def verify_passwords_matches(password1, password2):
    """Check that the passwords matches eachother."""
    return password1 == password2


def valid_email(email):
    """Check that the email-adress is valid."""
    email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return bool(email_re.match(email))
