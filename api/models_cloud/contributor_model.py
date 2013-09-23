#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel
from endpoints_proto_datastore.ndb import EndpointsAliasProperty


class Contributor(EndpointsModel):

    _message_fields_schema = ('name', 'job_position', 'company', 'google_plus', 'facebook', 'twitter', 'description', 'photo', 'id')

    name = ndb.StringProperty(required=True)
    job_position = ndb.StringProperty()
    company = ndb.StringProperty()
    google_plus = ndb.StringProperty()
    facebook = ndb.StringProperty()
    twitter = ndb.StringProperty()
    user = ndb.UserProperty(required=True)
    access_level = ndb.IntegerProperty()
    description = ndb.StringProperty()
    photo = ndb.StringProperty()

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Contributor, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()
