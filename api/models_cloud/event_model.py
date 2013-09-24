#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models_cloud.contributor_model import Contributor
import json

class Session (EndpointsModel):  #tuvimos que moverlo de session_model a event_model para evitar una puta referencia ciclica
                            #que anulaba toda la pagina

    title = ndb.StringProperty()
    overview = ndb.StringProperty()
    startTime = ndb.StringProperty()
    endTime = ndb.StringProperty()
    contributors = ndb.KeyProperty(kind=Contributor, repeated=True)
    contributors_id = ndb.StringProperty(repeated=True)

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Session, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

class Event (EndpointsModel):

    _message_fields_schema = 'id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid'

    title = ndb.StringProperty()
    description = ndb.StringProperty()
    date = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    gmap = ndb.StringProperty()
    flag = ndb.StringProperty()
    gplus_eventid = ndb.StringProperty()
    sessions = ndb.KeyProperty(kind=Session, repeated=True)
    sessions_id = ndb.StringProperty(repeated=True)

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Event, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

    @EndpointsAliasProperty() ######## NO FUNCIONA NI QUE LE PAGUES ¬¬ #######
    def full_sessions(self):
        data = []
        for session in self.sessions:
            session_add = Session.get_by_id(session.id())
            data.append({'title': session_add.title, 'overview': session_add.overview, 'startTime': session_add.startTime, 'endTime': session_add.endTime, 'contributors_id': session_add.contributors_id})
        return json.dumps(data)
