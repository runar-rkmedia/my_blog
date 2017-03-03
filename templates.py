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
from Entities import ArtEntity, BlogEntity, UserEntity, blog_key
from google.appengine.ext import db
from lib.pybcrypt import bcrypt  # This is slow, one should use regular bcrypt.

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True
)


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


def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def check_username_password(username, password):
    thisUserPath = db.Key.from_path('UserEntity', username)
    thisUser = db.get(thisUserPath)
    if thisUser:
        return bcrypt.hashpw(password, thisUser.password) == thisUser.password
    else:
        return False


class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, value, extra=""):
        self.response.headers.add_header(
            'Set-Cookie', '{}={}; {}'.format(name, value,extra))

    def delete_cookie(self, name):
        self.set_cookie(name,
                        'deleted',
                        'path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT')

    def perform_login(self, username):
        new_cookie_val = make_secure_val(str(username))
        self.set_cookie('user', new_cookie_val)

        self.redirect("/thanks?username=" + username)


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

        self.set_cookie('visits', new_cookie_val)

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
        username_cookie_val = self.request.cookies.get('user')
        username = None
        if username_cookie_val:
            cookie_val = check_secure_val(username_cookie_val)
            if cookie_val:
                username = cookie_val
        if not username:
            self.redirect('/signup')
        # username = self.request.get("username")
        self.render("/thanks.html", username=username)


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
        arts = db.GqlQuery("SELECT * FROM ArtEntity ORDER BY created DESC")
        self.render("ascii_chan.html", title=title,
                    art=art, error=error, arts=arts)

    def get(self):
        self.render_this()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = ArtEntity(title=title, art=art)
            a.put()
            self.redirect('/ascii_chan')
        else:
            error = "we need both a title and some artwork!"
            self.render_this(title=title, art=art, error=error)


class Login(Handler):

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        valid_login = check_username_password(username, password)

        if valid_login:
            self.perform_login(username)
        else:
            self.render("login.html",
                        error_invalid_login=True,
                        username=username,
                        )

class Logout(Handler):

    def get(self):
        self.delete_cookie('user')
        self.redirect('/signup')


class SignUp(Handler):

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
        username_already_in_use = not verify_signup.username_not_in_use(username)
        password_valid = verify_signup.valid_password(password)
        passwords_matches = verify_signup.verify_passwords_matches(
            password, verify)
        email_valid = verify_signup.valid_email(email)

        if email == "":
            email_valid = True
        if not(
            username_valid and
            not username_already_in_use and
            password_valid and
            passwords_matches and
            email_valid):
            self.render("signup.html",
                        username_valid=username_valid,
                        username_already_in_use=username_already_in_use,
                        password_valid=password_valid,
                        passwords_matches=passwords_matches,
                        email_valid=email_valid,
                        username=username,
                        email=email,
                        )
        else:
            password = hash_password(password)
            user = UserEntity(key_name=username, password=password,
                              email=email)
            user.put()

            self.perform_login(username)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/fizzbuzz', FizzBuzz),
    ('/rot13', Rot13),
    ('/signup', SignUp),
    ('/login', Login),
    ('/logout', Logout),
    ('/thanks', Thanks),
    ('/ascii_chan', AsciiChan),
    ('/new_blog_post', NewBlogPost),
    ('/blogs', Blogs),
    ('/blogs/(\d+)', BlogPost),
    ('/counter', VisitCounter),
], debug=True)
