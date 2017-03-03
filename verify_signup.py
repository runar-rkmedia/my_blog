#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db
# from Entities import UserEntity
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return bool(USER_RE.match(username))


def username_not_in_use(username):
    thisUserPath = db.Key.from_path('UserEntity', username)
    thisUser = db.get(thisUserPath)
    return not bool(thisUser)


def valid_password(password):
    return bool(PASS_RE.match(password))


def verify_passwords_matches(password1, password2):
    return password1 == password2


def valid_email(email):
    return bool(EMAIL_RE.match(email))
