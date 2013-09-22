#  coding: utf-8 --
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel
from api.models_cloud.contributor_model import Contributor
from api.models_cloud.comment_model import Comment


class Post(EndpointsModel):

    #POR DEFECTO DEVUELVE ESTO
    _message_fields_schema = ('id', 'title', 'author', 'description', 'cover', 'date', 'tags')

    title = ndb.StringProperty()
    authorkey = ndb.KeyProperty(kind=Contributor)
    description = ndb.StringProperty()
    content = ndb.StringProperty()  #va a explotar Textproperty
    cover = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)


    @EndpointsAliasProperty(required=True, property_type=Contributor.ProtoModel())
    def author(self):
        return ndb.get(self.authorkey)

    def IdSet(self, value):
        self.UpdateFromKey(ndb.Key(Post, str(value)))

    @EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
        if self.key is not None:
            return self.key.string_id()

    #@EndpointsAliasProperty() #### Problema, ahora que funciona traer la lista de Post, me devuelve también estos campos, y no quiero que en esa lista se devuelvan.
    #def autorcompleto(self):
    #    return json.dumps(self.author.get().to_dict())

    #@EndpointsAliasProperty()
    #def comentarioscompleto(self):
    #    post = Post.get_by_id(self.id)
    #    return json.dumps(improve(post.to_dict(exclude=["title","author","description","content","cover","date","tags"]))['comments'])
    #revisar por diferencia entre method y query_method al traer los comentarios
