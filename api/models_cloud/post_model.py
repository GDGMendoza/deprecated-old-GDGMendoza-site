#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models_cloud.contributor_model import Contributor
from api.models_cloud.comment_model import Comment


class Post(EndpointsModel):

    #POR DEFECTO DEVUELVE ESTO
    _message_fields_schema = ('id', 'title', 'author_id', 'description', 'cover', 'date', 'tags')

    title = ndb.StringProperty()
    author = ndb.KeyProperty(kind=Contributor)
    description = ndb.StringProperty()
    content = ndb.StringProperty()  #va a explotar Textproperty
    cover = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Post, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

    @EndpointsAliasProperty()
    def author_id(self):
        return self.author.get().id
