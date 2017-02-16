#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#

import os
import webapp2
import jinja2
from google.appengine.ext import db

#set up jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader =jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog_post = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        pass #replace this with some code to handle the request

class NewPost(Handler):
    #this generates
    def render_front(self, title="", blog_post="", error=""):
        self.render("front.html", title=title, blog_post=blog_post, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("blog_post")

        if title and blog_post:
            b = Blog(title=title, blog_post=blog_post)
            b.put()

            self.redirect("/blog")

        else:
            error = "we need both a title and a blog post!"
            self.render_front(title, blog_post, error = error)

class BlogPage(Handler):
    def render_blogpage(self, title=""):

        #this calls entered art from the database:
        posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")

        self.render("blog-page.html", title=title, posts=posts)

    def get(self):
        self.render_blogpage()



    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("blog_post")

        if title and blog_post:
            b = Blog(title=title, blog_post=blog_post)
            b.put()

            self.redirect("/blog")

app = webapp2.WSGIApplication([
        ('/blog', BlogPage),
        ('/newpost', NewPost)
    webapp2.Route('/blog/<post_id:\d+>', ViewPost)
], debug=True)

