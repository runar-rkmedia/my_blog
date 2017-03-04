"""Enities used in myBlog."""

from google.appengine.ext import db  # noqa
from lib.pybcrypt import bcrypt  # This is slow, one should use regular bcrypt.
import myExceptions


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
        existingUsername = UserEntity.by_name(username)
        if not existingUsername:
            if email == "":
                email = None
            password = UserEntity.hash_password(password)
            user = UserEntity(username=username, password=password,
                              email=email)
            user.put()
            return user
        else:
            raise myExceptions.NotUnique('Username is not unique')


class BlogEntity(db.Model):
    """Blog-entries."""
    title = db.StringProperty(required=True)
    article = db.TextProperty(required=True)
    created_by = db.ReferenceProperty(UserEntity, required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    # def by_id(cls, blog_id):
    #     """Retrieve a blogentry by its id."""
    #     blogEntry = db.Key.from_path('BlogEntity', blog_key())
    #     return blogEntry
    @classmethod
    def by_title(cls, title):
        """Retrieve a blogentry by its title."""
        blogEntry = BlogEntity.all().filter('title =', title).get()
        return blogEntry

    @classmethod
    def create_blog_entry(cls, parent, title, article, created_by):
        """Create a blog entry, verify data first."""
        exisistingTitle = BlogEntity.by_title(title)
        print created_by
        if not exisistingTitle:
            blogEntry = BlogEntity(parent=parent,
                                   title=title,
                                   article=article,
                                   created_by=created_by)
            blogEntry.put()
            return blogEntry
        else:
            raise myExceptions.NotUnique('Title of blog needs to be unique')


def blog_key(name='default'):
    """helper-function."""
    return db.Key.from_path('blogs', name)


class VotesEntity(db.Model):
    """Votes in the blog."""

    voteBy = db.ReferenceProperty(UserEntity, required=True)
    voteOn = db.ReferenceProperty(BlogEntity, required=True)
    voteType = db.StringProperty(required=True, choices=('up', 'down'))

    @classmethod
    def get_votes_on_post(cls, voteOn):
        """Return up- and downvotes for the blog_post."""
        upvotes = VotesEntity.all().filter(
            'voteOn = ', voteOn).filter('voteType = ', 'up').count()
        downvotes = VotesEntity.all().filter(
            'voteOn = ', voteOn).filter('voteType = ', 'down').count()
        return upvotes, downvotes

    @classmethod
    def get_votes_by_user(cls, voteBy):
        """Return all voteEntries by user."""
        return VotesEntity.all().filter('voteBy = ', voteBy).get()

    @classmethod
    def get_vote_by_user_on_post(cls, voteBy, voteOn):
        """Return all voteEntries by user."""
        vote_entry = VotesEntity.all().filter(
            'voteBy = ', voteBy).filter(
                'voteOn = ', voteOn).get()
        if vote_entry:
            return vote_entry.voteType

    @classmethod
    def vote_on_blog(cls, voteOn, voteBy, voteType):
        """
        Update a vote, or create it if it doesn't exist.

        Users can only vote once, so only one record per blog per user.
        """
        vote_entry = VotesEntity.all().filter(
            'voteBy = ', voteBy).filter(
                'voteOn = ', voteOn).get()
        if vote_entry:
            vote_entry.voteType = voteType
            vote_entry.put()
        else:
            vote_entry = VotesEntity(
                voteBy=voteBy,
                voteOn=voteOn,
                voteType=voteType).put()
        return vote_entry
