#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models.contributor_model import Contributor

class Comment(EndpointsModel):

    author = ndb.KeyProperty(kind=Contributor)
    content = ndb.StringProperty() #### NO ESTA SOPORTANDO TextProperty ####
    date = ndb.DateTimeProperty(auto_now_add=True)

class Post(EndpointsModel):

    title = ndb.StringProperty()
    author = ndb.KeyProperty(kind=Contributor)
    description = ndb.StringProperty()
    content = ndb.StringProperty() #### NO ESTA SOPORTANDO TextProperty ####
    cover = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Post, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

