#  coding: utf-8 --
from api.lib import bottle
from api.lib.bottle import *
from api.models.contributor_model import Contributor
from google.appengine.ext import ndb

def initRoutes(app=None):
    if not app:
        app = bottle.default_app()

    @app.route('/contributor/getContributorList', method='POST')
    def getContributorList():                                           #testeado y andando!
        return Contributor.get_all_json()
        #return [post.to_dict() for post in Post.query()]

    @app.route('/contributor/getContributor', method='POST')
    def getContributor():                                               #testeado y andando!
        return Contributor.get_id_json(request.json["id"])

    @app.route('/put/contributor', method='POST')                       #testeado y andando!
    def putContributor():
        Contributor.put_contributor(
            id_query = request.json["id"],
            name = request.json["name"],
            photo = request.json["photo"],
            description = request.json["description"],
            email = request.json["email"],
            gplus = request.json["gplus"],
            fb = request.json["fb"],
            tw = request.json["tw"]
        )
        return "Contributor agregado exitosamente!"

    @app.route('/edit/contributor', method='POST')                      #testeado y andando! (esta igual que el put)
    def editContributor():
        Contributor.put_contributor(
            id_query = request.json["id"],
            name = request.json["name"],
            photo = request.json["photo"],
            description = request.json["description"],
            email = request.json["email"],
            gplus = request.json["gplus"],
            fb = request.json["fb"],
            tw = request.json["tw"]
        )
        return "Contributor editado exitosamente!"

    @app.route('/remove/contributor', method='POST')
    def removeContributor():                                            #testeado y andando!
        Contributor.remove_contributor(request.json["id"])
        return "Contributor eliminado exitosamente!"
