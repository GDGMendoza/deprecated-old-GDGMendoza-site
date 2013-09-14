#  coding: utf-8 --
from api.lib import bottle
from api.lib.bottle import *
from api.models.event_model import Event, Session


def initRoutes(app=None):
    if not app:
        app = bottle.default_app()

    @app.route('/events/getEventList', method='POST')
    def getEventList():                                         #testeado y andando!
        return Event.get_all_json()#[post.to_dict() for post in Post.query()]

    @app.route('/events/getEvent', method='POST')
    def getEvent():                                             #testeado y andando!
        return Event.get_id_json(request.json["id"])

    @app.route('/put/event', method='POST')
    def putEvent():                                             #testeado y andando!
        Event.put_event(
            id_query = request.json["id"],
            title = request.json["title"],
            description = request.json["description"],
            date = request.json["date"],
            tags = request.json["tags"], #cuidado que es un arreglo
            gmap = request.json["gmap"],
            gplus_eventid = request.json["gplus_eventid"]
        )
        return "Event agregado exitosamente!"

    @app.route('/edit/event', method='POST')
    def editEvent():                                            #testeado y andando!
        Event.put_event(
            id_query = request.json["id"],
            title = request.json["title"],
            description = request.json["description"],
            date = request.json["date"],
            tags = request.json["tags"],
            gmap = request.json["gmap"],
            gplus_eventid = request.json["gplus_eventid"]
        )
        return "Event editado exitosamente!"

    @app.route('/remove/event', method='POST')
    def removeEvent():                                          #testeado y andando!
        Event.remove_event(request.json["id"])
        return "Event eliminado exitosamente!"

    @app.route('/events/getSessionList', method='POST')
    def getSessionList():                                         #testeado y andando!
        return Session.get_all_json()#[post.to_dict() for post in Post.query()]

    @app.route('/events/getSession', method='POST')
    def getSession():                                             #testeado y andando!
        return Session.get_id_json(request.json["id"])

    @app.route('/put/session', method='POST')
    def putSession():                                             #testeado y andando!
        Session.put_session(
            id_query = request.json["id"],
            title = request.json["title"],
            overview = request.json["overview"],
            startTime = request.json["startTime"],
            endTime = request.json["endTime"],
            contributors = request.json["contributors"]
        )
        return "Session agregada exitosamente!"

    @app.route('/edit/session', method='POST')
    def editSession():                                          #testeado y andando!
        Session.put_session(
            id_query = request.json["id"],
            title = request.json["title"],
            overview = request.json["overview"],
            startTime = request.json["startTime"],
            endTime = request.json["endTime"],
            contributors = request.json["contributors"]
        )
        return "Session editada exitosamente!"

    @app.route('/remove/session', method='POST')
    def removeSession():                                        #testeado y andando!
        Session.remove_session(request.json["id"])
        return "Session eliminada exitosamente!"

    @app.route('/remove/sessionFromEvent', method='POST')
    def removeSessionFromEvent():                               #testeado y andando!
        Session.remove_session_from_event(
            id_event = request.json["id_event"],
            id_session = request.json["id_session"]
        )
        return "Session eliminada exitosamente del evento!"

    @app.route('/put/sessionInEvent', method='POST')
    def putSessionInEvent():                                        #testeado y andando!
        Session.append_session(
            id_event=request.json["id_event"],
            id_session=request.json["id_session"]
        )
        return "Session agregada exitosamente al evento!"

