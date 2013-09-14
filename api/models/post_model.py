#  coding: utf-8 --
from google.appengine.ext import ndb
from google.appengine.ext.ndb.key import Key
from api.lib import date_handler
from api.lib.bottle import json_dumps
from api.models.contributor_model import Contributor
from api.lib.bottle import *
from api.lib.date_handler import date_handler
from api.lib.custom_handler import improve


class Comment(ndb.Model):

    author = ndb.KeyProperty(kind=Contributor)
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def put_comment(self, id_query, author, content):
        post = Post.get_by_id(id_query)
        post.comments.append(Comment(author=Key("Contributor", author), content=content))
        return post.put()

class Post(ndb.Model):

    title = ndb.StringProperty()
    author = ndb.KeyProperty(kind=Contributor)
    description = ndb.StringProperty()
    content = ndb.TextProperty()
    cover = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    @classmethod
    def get_all_json(self):
        return json_dumps([improve(post.to_dict(exclude=["comments"]), post.key.id()) for post in Post.query()], default=date_handler)

    @classmethod
    def get_id_json(self, id_query):
        post = Post.get_by_id(id_query)
        return json_dumps(improve(post.to_dict(),identificador=post.key.id()), default=date_handler)

    @classmethod
    def put_post(self, id_query, title, author, description, content, cover, tags):
        return Post(
            id = id_query,
            title = title,
            author = Key("Contributor", author),
            description = description,
            content = content,
            cover = cover,
            tags = tags
        ).put()

    @classmethod
    def remove_post(self, id_query):
        return Key("Post", id_query).delete()
