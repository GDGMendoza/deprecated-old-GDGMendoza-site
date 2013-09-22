#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models_cloud.contributor_model import Contributor


class Comment(EndpointsModel):

    author = ndb.KeyProperty(kind=Contributor)
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)