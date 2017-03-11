"""Enities used in myBlog."""

import datetime
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
    def by_title(cls, title):
        """Retrieve a blogentry by its title."""
        blogEntry = BlogEntity.all().filter('title =', title).get()
        return blogEntry

    @classmethod
    def get_by_id_str(cls, blog_id):
        """Return a blog_entry from blog_id(str) if valid."""
        if blog_id.isdigit():
            return BlogEntity.get_by_id(int(blog_id), parent=blog_key())

    @classmethod
    def create_blog_entry(cls, parent, title, article, created_by):
        """Create a blog entry, verify data first."""
        existingTitle = BlogEntity.by_title(title)
        if not existingTitle:
            blogEntry = BlogEntity(parent=parent,
                                   title=title,
                                   article=article,
                                   created_by=created_by)
            blogEntry.put()
            return blogEntry
        else:
            raise myExceptions.NotUnique('Title of blog needs to be unique')

    def edit_blog_entry(self, title, article, created_by):
        """Edit a blog entry, verify data first."""
        existingTitle = BlogEntity.by_title(title)
        if existingTitle and existingTitle.key().id() != self.key().id():
            raise myExceptions.NotUnique('Title of blog needs to be unique')
        elif created_by.key().id() == self.created_by.key().id():
            self.title = title
            self.article = article
            self.last_modified = datetime.datetime.now()
            self.put()
            return self
        else:
            raise myExceptions.EditOthersPosts(
                'You do not have access to edit this post.')

    def delete_post(self, user):
        """Delete this post, and all comments and votes related to it."""
        if user.key().id() == self.created_by.key().id():
            blog_entry_votes = VotesEntity.all().filter('voteOn = ', self)
            blog_entry_comments = CommentsEntity.all().filter('commentOn = ', self)
            db.delete(blog_entry_votes)
            db.delete(blog_entry_comments)
            db.delete(self)
        else:
            raise myExceptions.EditOthersPosts(
                'You do not have access to delete this post.')

    def getVotes(self):
        """Return all votes on this post."""
        return VotesEntity.get_votes_on_post(self)

    def vote(self, voteBy, voteType):
        """Vote on this blog."""
        return VotesEntity.vote_on_blog(
            voteOn=self, voteBy=voteBy, voteType=voteType)

    def getVotesFromUser(self, user):
        """Return voteType('up', or 'down') on this post by this user."""
        return VotesEntity.get_vote_by_user_on_post(voteOn=self, voteBy=user)

    def output_html_article(self):
        """Return an html-friendly version of the article."""
        return self.article.replace('\n', '<br>')  # noqa

    def add_comment(self, commentBy, comment):
        """Create a comment on this post."""
        return CommentsEntity.comment_on_post(
            commentOn=self, commentBy=commentBy, comment=comment)

    def get_comments(self):
        """Return all comments on this post."""
        comments = CommentsEntity.get_comments_on_post(commentOn=self)
        return comments


def blog_key(name='default'):
    """helper-function."""
    return db.Key.from_path('blogs', name)


class CommentsEntity(db.Model):
    """Comments for blog_entries"""

    commentBy = db.ReferenceProperty(UserEntity, required=True)
    commentOn = db.ReferenceProperty(BlogEntity, required=True)
    comment = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_by_id_str(cls, comment_id):
        """Return a blog_entry from comment_id(str) if valid."""
        if comment_id.isdigit():
            return CommentsEntity.get_by_id(int(comment_id))

    @classmethod
    def verify_comment(cls, comment):
        """Verify that the comment is valid."""
        return len(comment) > 2

    @classmethod
    def comment_on_post(cls, commentBy, commentOn, comment):
        """Create a comment."""
        comment = comment.strip()
        if not CommentsEntity.verify_comment(comment):
            raise myExceptions.TooShort("Comment is too short.")
        comment_entry = CommentsEntity(
            commentBy=commentBy,
            commentOn=commentOn,
            comment=comment)
        comment_entry.put()
        return comment_entry

    @classmethod
    def get_comments_on_post(cls, commentOn):
        """Return comments for the blog_post."""
        comments = CommentsEntity.all().filter(
            'commentOn = ', commentOn)
        return comments

    def edit_comment(self, comment, commentBy):
        """Change the comment(text)."""
        if commentBy.key().id() != self.commentBy.key().id():
            raise myExceptions.EditOthersComments(
                "You don't have access to editing this post")
        if not CommentsEntity.verify_comment(comment):
            raise myExceptions.TooShort("Comment is too short")
        self.comment = comment.strip()
        self.put()
        return self


class VotesEntity(db.Model):
    """Votes in the blog."""

    voteBy = db.ReferenceProperty(UserEntity, required=True)
    voteOn = db.ReferenceProperty(BlogEntity, required=True)
    voteType = db.StringProperty(required=True, choices=('up', 'down'))

    @classmethod
    def get_votes_on_post(cls, voteOn):
        """Return up- and downvotes for the blog_post."""
        votes = {}
        votes['up'] = VotesEntity.all().filter(
            'voteOn = ', voteOn).filter('voteType = ', 'up').count()
        votes['down'] = VotesEntity.all().filter(
            'voteOn = ', voteOn).filter('voteType = ', 'down').count()
        return votes

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
        They also cannot vote on their own posts.
        """
        if voteOn.created_by.key().id() == voteBy.key().id():
            raise myExceptions.VoteOnOwnPostNotAllowed(
                'Cannot vote on own post')
        vote_entry = VotesEntity.all().filter(
            'voteBy = ', voteBy).filter(
                'voteOn = ', voteOn).get()
        if vote_entry:
            if vote_entry.voteType == voteType:
                vote_entry.delete()
            else:
                vote_entry.voteType = voteType
                vote_entry.put()
        else:
            vote_entry = VotesEntity(
                voteBy=voteBy,
                voteOn=voteOn,
                voteType=voteType).put()
        return vote_entry
