#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel

class Contributor(EndpointsModel):

    name = ndb.StringProperty()
    photo = ndb.StringProperty()
    description = ndb.StringProperty()
    email = ndb.StringProperty()
    gplus = ndb.StringProperty()
    fb = ndb.StringProperty()
    tw = ndb.StringProperty()

