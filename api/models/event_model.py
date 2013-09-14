#  coding: utf-8 --
from google.appengine.ext import ndb
from google.appengine.ext.ndb.key import Key
from api.lib.custom_handler import improve
from api.lib.date_handler import date_handler
from api.lib.bottle import json_dumps
from api.models.contributor_model import Contributor


class Session (ndb.Model):  #tuvimos que moverlo de session_model a event_model para evitar una puta referencia ciclica
                            #que anulaba toda la pagina

    title = ndb.StringProperty()
    overview = ndb.StringProperty()
    startTime = ndb.StringProperty()
    endTime = ndb.StringProperty()
    contributors = ndb.KeyProperty(kind=Contributor, repeated=True)

    @classmethod
    def get_all_json(self):
        return json_dumps([improve(session.to_dict(), session.key.id()) for session in Session.query()], default=date_handler)

    @classmethod
    def get_id_json(self, id_query):
        session = Session.get_by_id(id_query)
        return json_dumps(improve(session.to_dict(),identificador=session.key.id()), default=date_handler)

    @classmethod
    def put_session(self, id_query, title, overview, startTime, endTime, contributors):
        return Session(id=id_query, title=title, overview=overview, startTime=startTime, endTime=endTime, contributors=[Key("Contributor", contributor) for contributor in contributors]).put()

    @classmethod
    def append_session(self, id_event, id_session):
        event = Event.get_by_id(id_event)
        flag = True
        for item in event.sessions:
            if item == Key("Session", id_session):
                flag = False
        if flag:
            event.sessions.append(Key("Session", id_session))
        #if event.sessions.index(Key("Session", id_session)) == -1 :
        #    event.sessions.append(Key("Session", id_session))
        return event.put()

    @classmethod
    def remove_session_from_event(self, id_event, id_session):
        event = Event.get_by_id(id_event)
        event.sessions.remove(Key("Session", id_session))
        return event.put()

    @classmethod
    def remove_session(self, id_query):
        return Key("Session", id_query).delete()


class Event (ndb.Model):

    title = ndb.StringProperty()
    description = ndb.StringProperty()
    date = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    gmap = ndb.StringProperty()
    flag = ndb.StringProperty()
    gplus_eventid = ndb.StringProperty()
    sessions = ndb.KeyProperty(kind=Session, repeated=True)
    #id usuario en gplus donde se encuentran las fotos del evento
    #id del album de ese usuario donde estan las fotos

    @classmethod
    def get_all_json(self):
        return json_dumps([improve(event.to_dict(), event.key.id()) for event in Event.query()], default=date_handler)

    @classmethod
    def get_id_json(self, id_query):
        event = Event.get_by_id(id_query)
        return json_dumps(improve(event.to_dict(),identificador=event.key.id()), default=date_handler)

    @classmethod
    def put_event(self, id_query, title, description, date, tags, gmap, gplus_eventid):
        return Event(
            id = id_query,
            title = title,
            description = description,
            date = date,
            tags = tags, #cuidado que este deberia ser un array
            gmap = gmap,
            gplus_eventid = gplus_eventid
        ).put()

    @classmethod
    def remove_event(self, id_query):
        return Key("Event", id_query).delete()
