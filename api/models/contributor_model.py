#  coding: utf-8 --
from google.appengine.ext import ndb
from google.appengine.ext.ndb.key import Key
from api.lib.custom_handler import improve
from api.lib.date_handler import date_handler
from api.lib.bottle import json_dumps


class Contributor(ndb.Model):

    name = ndb.StringProperty()
    photo = ndb.StringProperty()
    description = ndb.StringProperty()
    email = ndb.StringProperty()
    gplus = ndb.StringProperty()
    fb = ndb.StringProperty()
    tw = ndb.StringProperty()


    @classmethod
    def get_all_json(self):
        return json_dumps([improve(contributor.to_dict(), contributor.key.id()) for contributor in Contributor.query()], default=date_handler)

    @classmethod
    def get_id_json(self, id_query):
        contributor = Contributor.get_by_id(id_query)
        return json_dumps(improve(contributor.to_dict(),identificador=contributor.key.id()), default=date_handler)

    @classmethod
    def put_contributor(self, id_query, name, photo, description, email, gplus, fb, tw):
        return Contributor(
            id = id_query,
            name = name,
            photo = photo,
            description = description,
            email = email,
            gplus = gplus,
            fb = fb,
            tw = tw
        ).put()

    @classmethod
    def remove_contributor(self, id_query):
        return Key("Contributor", id_query).delete()
