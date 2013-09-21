#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models.contributor_model import Contributor
from api.lib.custom_handler import improve
import json

class Comment(EndpointsModel):

    author = ndb.KeyProperty(kind=Contributor)
    content = ndb.StringProperty() #### NO ESTA SOPORTANDO TextProperty ####
    date = ndb.DateTimeProperty(auto_now_add=True)

class Post(EndpointsModel):

    _message_fields_schema = ('id','title','author','description','cover','date','tags') ######## POR DEFECTO DEVUELVE ESTO #######

    title = ndb.StringProperty()
    author = ndb.KeyProperty(kind=Contributor)
    description = ndb.StringProperty()
    content = ndb.StringProperty() #### NO ESTA SOPORTANDO TextProperty ####
    cover = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    @classmethod
    def remove_post(self, id_query):
        return ndb.Key("Post", id_query).delete()

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Post, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

    @EndpointsAliasProperty() #### Problema, ahora que funciona traer la lista de Post, me devuelve también estos campos, y no quiero que en esa lista se devuelvan.
    def autorcompleto(self):
        return json.dumps(self.author.get().to_dict())

    @EndpointsAliasProperty()
    def comentarioscompleto(self):
        post = Post.get_by_id(self.id)
        return json.dumps(improve(post.to_dict(exclude=["title","author","description","content","cover","date","tags"]))['comments'])

