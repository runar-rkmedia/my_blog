from google.appengine.ext import db
from lib.pybcrypt import bcrypt  # This is slow, one should use regular bcrypt.


class ArtEntity(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class BlogEntity(db.Model):
    title = db.StringProperty(required=True)
    article = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now_add=True)

    def render(self):
        self._render_text = self.article.replace('\n', '<br>')
        return render_str("view_blog_entry.html", blog_entry=self)


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class UserEntity(db.Model):
    email = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    password = db.StringProperty(required=True)
    username = db.StringProperty(required=True)

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def check_username_password(cls, username, password):
        thisUser = UserEntity.by_name(username)
        if thisUser and bcrypt.hashpw(
                password,
                thisUser.password) == thisUser.password:
            return thisUser


    @classmethod
    def by_name(cls, username):
        thisUser = UserEntity.all().filter('username =', username).get()
        return thisUser

    @classmethod
    def register(cls, username, password, email=None):
        if email == "":
            email = None
        password = UserEntity.hash_password(password)
        user = UserEntity(username=username, password=password,
                          email=email)
        user.put()
        return user
