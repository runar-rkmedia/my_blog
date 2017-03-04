"""Enities used in myBlog."""

from google.appengine.ext import db # noqa
from lib.pybcrypt import bcrypt  # This is slow, one should use regular bcrypt.



class UserEntity(db.Model):
    """Useraccounts."""
    email = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    password = db.StringProperty(required=True)
    username = db.StringProperty(required=True)

    @classmethod
    def hash_password(cls, password):
        """Create a secure hash of password using bcrypt"""
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def check_username_password(cls, username, password):
        """Chech a secure hash of a password against a user using bcrypt."""
        thisUser = UserEntity.by_name(username)
        if thisUser and bcrypt.hashpw(
                password,
                thisUser.password) == thisUser.password:
            return thisUser

    @classmethod
    def by_name(cls, username):
        """Retrieve a useraccount by its name."""
        thisUser = UserEntity.all().filter('username =', username).get()
        return thisUser

    @classmethod
    def register(cls, username, password, email=None):
        """Register a useraccount in the datastores."""
        if email == "":
            email = None
        password = UserEntity.hash_password(password)
        user = UserEntity(username=username, password=password,
                          email=email)
        user.put()
        return user


class BlogEntity(db.Model):
    """Blog-entries."""
    title = db.StringProperty(required=True)
    article = db.TextProperty(required=True)
    created_by = db.ReferenceProperty(UserEntity, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)


def blog_key(name='default'):
    """helper-function."""
    # TODO: Could probably remove this
    return db.Key.from_path('blogs', name)
