"""myBlog, an assignment on Udacity (Full Stack)."""

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

import os
from math import ceil
import jinja2
import webapp2
import verify_signup
from hash_functions import make_secure_val, check_secure_val
from Entities import BlogEntity, UserEntity, blog_key
import myExceptions
# import test_data

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True
)


class Handler(webapp2.RequestHandler):
    """Handler for the different landingpages."""

    def write(self, *a, **kw):
        """Web response."""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """???."""
        # TODO: Remove/rename this. Confusing.
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        username = self.read_secure_cookie('user')
        kw['signed_in'] = username
        self.write(self.render_str(template, **kw))

    def set_cookie(self, name, value, extra=""):
        """Create a cookie."""
        self.response.headers.add_header(
            'Set-Cookie', '{}={}; {}'.format(name, value, extra))

    def set_secure_cookie(self, name, value, extra=""):
        """Create a secure cookie in the browser."""
        value = make_secure_val(str(value))
        self.set_cookie(name, value, extra)

    def read_cookie(self, name):
        """Read a cookie from the browser."""
        return self.request.cookies.get(name)

    def read_secure_cookie(self, name):
        """Read a secure cookie from the browser."""
        cookie_value = self.read_cookie(name)
        return cookie_value and check_secure_val(cookie_value)

    def delete_cookie(self, name):
        """Delete a cookie from the browser."""
        self.set_cookie(name,
                        'deleted',
                        'path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'
                        )  # noqa

    def perform_login(self, username):
        """Set the user-cookie in the browser and redirect."""
        new_cookie_val = make_secure_val(str(username))
        self.set_cookie('user', new_cookie_val)

        self.redirect("/thanks?redirect=/welcome")

    def initialize(self, *a, **kw):
        """Retrieve the user-cookier on every new page-load."""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        username = self.read_secure_cookie('user')
        if username:
            self.user = UserEntity.by_name(username)  # noqa
        else:
            self.user = False  # noqa

    def render_blog_article(self, article):
        """Render an html-element for a single blog-entry."""
        self._render_text = article.article.replace('\n', '<br>')  # noqa
        return self.render_str("view_blog_entry.html", blog_entry=article)

    def render_page_buttons(self, pages, currentPage):
        """Render an html-element for a page-navigation."""
        return self.render_str("page-buttons.html",
                               pages=pages,
                               currentPage=currentPage)


class Welcome(Handler):
    """Welcome message for user."""

    def get(self):
        """Show the welcome-message with the username."""
        self.render("/welcome.html", username=self.user.username)


class Thanks(Handler):
    """Redirection page"""

    def get(self):
        """Show the redirection-page."""
        redirect = self.request.get("redirect")
        self.render("/thanks.html", redirect=redirect)


class Blogs(Handler):
    """Show a list of the latest blogs."""

    def get(self):
        """Retrieve all the latest blog-entries and render them to user."""
        page_to_show = self.request.get("page")
        if page_to_show.isdigit() and int(page_to_show) > 1:
            page_to_show = int(page_to_show)
        else:
            page_to_show = 1

        limit = 10
        offset = (page_to_show - 1) * limit
        totalArticles = BlogEntity.all().count(1000)
        totalPages = int(ceil(float(totalArticles) / limit))
        articles = BlogEntity.all().order('-created').fetch(limit=limit, offset=offset)
        self.render("blogs.html", articles=articles,
                    parser=self.render_blog_article,
                    pageButtons=self.render_page_buttons(totalPages, page_to_show))


class BlogPost(Handler):
    """Show a single blog-entry."""

    def get(self, blog_id):
        """Retrieve the blog-id from the url and shw it."""
        if blog_id.isdigit():
            blog_id = int(blog_id)
            blog_entry = BlogEntity.get_by_id(blog_id, parent=blog_key())
        else:
            blog_id = urllib.unquote(blog_id)
            print blog_id
            blog_entry = BlogEntity.by_title('Create new blog posts')

        if not blog_entry:
            self.error(404)
            return

        self.render("blog_permalink.html", article=blog_entry,
                    parser=self.render_blog_article)


class NewBlogPost(Handler):
    """View for creating a new post."""

    def render_this(self, title="", article="", **kw):
        """Renders the 'new blog'-form, but only if the user is logged in."""
        if self.user:
            print kw
            self.render("new_blog_post.html", title=title,
                        article=article, **kw)
        else:
            self.redirect("/login")

    def get(self):
        """Renders the 'new blog'-form, but only if the user is logged in."""
        self.render_this()

    def post(self):
        """Create a blog-entry if logged in and form filled out correcly."""
        if not self.user:
            self.redirect('/login')
        else:
            title = self.request.get("title").strip()
            article = self.request.get("article")
            if title and article and self.user:
                try:
                    a = BlogEntity.create_blog_entry(parent=blog_key(),
                                                     created_by=self.user,
                                                     title=title,
                                                     article=article)
                    self.redirect('/blogs/%s' % str(a.key().id()))
                except myExceptions.NotUnique as e:
                    self.render_this(title=title, article=article, error_notUnique=True)
            else:
                self.render_this(title=title, article=article, error_missing_fields=True)


class Login(Handler):
    """Login user."""

    def get(self):
        """View for login-screen."""
        self.render("login.html")

    def post(self):
        """Log in user(set cookie) if user and password matches."""
        username = self.request.get("username")
        password = self.request.get("password")

        valid_login = UserEntity.check_username_password(username, password)

        if valid_login:
            self.perform_login(username)
        else:
            self.render("login.html",
                        error_invalid_login=True,
                        username=username,
                        )  # noqa


class Logout(Handler):
    """Logout user."""

    def get(self):
        """Delete usercookie to logout user."""
        self.delete_cookie('user')
        self.redirect('/signup')


class SignUp(Handler):
    """View for sign-up-form."""

    def get(self):
        """Show the sign-up-form."""
        self.render("signup.html",
                    username_valid=True,
                    password_valid=True,
                    passwords_matches=True,
                    email_valid=True,
                    )  # noqa

    def post(self):
        """Register the user if form is filled out correctly."""
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
        if not(
                username_valid and
                password_valid and
                passwords_matches and
                email_valid):
            self.render("signup.html",
                        error_username_invalid=not username_valid,
                        error_password_invalid=not password_valid,
                        error_passwords_mismatch=not passwords_matches,
                        error_email_invalid=not email_valid,
                        username=username,
                        email=email,
                        )  # noqa
        else:
            try:
                UserEntity.register(username, password, email)
                self.perform_login(username)
            except myExceptions.NotUnique:
                self.render("signup.html",
                            errro_username_already_in_use=True,
                            username=username,
                            email=email,
                            )  # noqa


app = webapp2.WSGIApplication([
    ('/', Blogs),
    ('/signup', SignUp),
    ('/login', Login),
    ('/logout', Logout),
    ('/thanks', Thanks),
    ('/welcome', Welcome),
    ('/new_blog_post', NewBlogPost),
    ('/blogs', Blogs),
    ('/blogs/(\d+)', BlogPost),  # noqa
], debug=True)
