#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models_cloud.contributor_model import Contributor


class Comment(EndpointsModel):

    _message_fields_schema = ('content', 'date', 'author_id')

    author = ndb.KeyProperty(kind=Contributor)
    content = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    post_id = ndb.StringProperty() ####### MI SUPER VARIABLE AUXILIAR !! By Cristian ;) ########

    @EndpointsAliasProperty()
    def author_id(self):
        return self.author.get().id
