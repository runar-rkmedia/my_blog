from google.appengine.ext import db

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
