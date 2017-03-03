# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hmac
import os
import jinja2
import webapp2
import rot13
import verify_signup
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True
)


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def hash_str(s):
    # TODO: Should use bcrypt
    secret = "fd4c2d860910b3a7b65c576d247292e8"
    return hmac.new(secret, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class VisitCounter(Handler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visits_cookie_val = self.request.cookies.get('visits')
        print visits_cookie_val
        if visits_cookie_val:
            cookie_val = check_secure_val(visits_cookie_val)
            if cookie_val:
                visits = int(cookie_val)

        visits += 1

        new_cookie_val = make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie', 'visits={}'.format(new_cookie_val))

        self.write("You've been here %s times" % visits)


class MainPage(Handler):

    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)


class FizzBuzz(Handler):

    def get(self):
        n = self.request.get("n")
        if n and n.isdigit():
            n = int(n)
        self.render("fizzbuzz.html", n=n)


class Rot13(Handler):

    def get(self):
        self.render("rot13.html")

    def post(self):
        text = self.request.get("text")
        text = rot13.rot_13(text)
        self.render("rot13.html", text=text)


class Thanks(Handler):

    def get(self):
        username = self.request.get("username")
        self.render("thanks.html", username=username)


class Art(db.Model):
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


class Blogs(Handler):

    def render_this(self):
        articles = BlogEntity.all().order('-created')
        self.render("blogs.html", articles=articles)

    def get(self):
        self.render_this()


class BlogPost(Handler):

    def render_this(self, blog_entry):
        self.render("view_blog_entry.html", blog_entry=blog_entry)

    def get(self, blog_id):
        blog_id = int(blog_id)
        blog_entry = BlogEntity.get_by_id(blog_id, parent=blog_key())
        if not blog_entry:
            self.error(404)
            return

        self.render_this(blog_entry)


class NewBlogPost(Handler):

    def render_this(self, title="", article="", error=""):
        self.render("new_blog_post.html", title=title,
                    article=article, error=error)

    def get(self):
        self.render_this()

    def post(self):
        title = self.request.get("title")
        article = self.request.get("article")

        if title and article:
            a = BlogEntity(parent=blog_key(), title=title, article=article)
            a.put()
            self.redirect('/blogs/%s' % str(a.key().id()))
        else:
            error = "we need both a title and an article!"
            self.render_this(title=title, article=article, error=error)


class AsciiChan(Handler):

    def render_this(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("ascii_chan.html", title=title,
                    art=art, error=error, arts=arts)

    def get(self):
        self.render_this()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)
            a.put()
            self.redirect('/ascii_chan')
        else:
            error = "we need both a title and some artwork!"
            self.render_this(title=title, art=art, error=error)


class SighUp(Handler):

    def get(self):
        self.render("signup.html",
                    username_valid=True,
                    password_valid=True,
                    passwords_matches=True,
                    email_valid=True,
                    )

    def post(self):
        username = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        verify = self.request.get("verify")

        username_valid = verify_signup.valid_username(username)
        password_valid = verify_signup.valid_password(password)
        passwords_matches = verify_signup.verify_passwords_matches(
            password, verify)
        email_valid = verify_signup.valid_email(email)

        if email == "":
            email_valid = True
        if not(username_valid and password_valid and passwords_matches and email_valid):
            self.render("signup.html",
                        username_valid=username_valid,
                        password_valid=password_valid,
                        passwords_matches=passwords_matches,
                        email_valid=email_valid,
                        username=username,
                        email=email,
                        )
        else:
            self.redirect("/thanks?username=" + username)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzz),
    ('/rot13', Rot13),
    ('/signup', SighUp),
    ('/thanks', Thanks),
    ('/ascii_chan', AsciiChan),
    ('/new_blog_post', NewBlogPost),
    ('/blogs', Blogs),
    ('/blogs/(\d+)', BlogPost),
    ('/counter', VisitCounter),
], debug=True)
