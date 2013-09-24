# -*- coding: utf-8 -*-
from google.appengine.ext import endpoints
from protorpc import remote
from google.appengine.ext import ndb

##################### MODELS ########################
from api.models_cloud.post_model import Post
from api.models_cloud.comment_model import Comment
from api.models_cloud.contributor_model import Contributor
from api.models_cloud.event_model import Session, Event

################################################ CLOUD ENDPOINTS SERVICE  ##############################################
@endpoints.api(name='gdgmendoza', version='v1',
               description='API for GDG Mendoza Management')
class GDGMendozaAPI(remote.Service):
############## CONTRIBUTOR ################
    @Contributor.method(name='contributor.insert', ########### FUNCIONA ############
                        path='contributor',
                        user_required=True)
    def insert_contributor(self, contributor):
        contributor.user = endpoints.get_current_user()
        contributor.id = contributor.user.email()
        if contributor.from_datastore:
            raise endpoints.BadRequestException( 'User %s already exists.' % (contributor.id,))
        contributor.access_level = 1
        contributor.put()
        return contributor

    @Contributor.query_method(name='contributor.list', ########### FUNCIONA ############
                              path='contributor')
    def contributor_list(self, query):
        return query

    ################## POST #####################
    @Post.method(name='post.insert', ########### FUNCIONA ############
                 path='post',
                 user_required=True)
    def insert_post(self, post):
        if post.from_datastore:
            name = post.key.string_id()
            raise endpoints.BadRequestException( 'Post of name %s already exists.' % (name,))
        post.author = ndb.Key(Contributor, endpoints.get_current_user().email())
        post.put()
        return post

    @Post.method(name='post.delete', ########### FUNCIONA ############
                 path='deletepost/{id}',
                 response_fields=('id',)) ####### Devuelve el ID cuando se borro correctamente #######
    def delete_post(self, post):
        if post.from_datastore:
            Post.Key("Post", post.id).delete()
        else:
            raise endpoints.NotFoundException('Post not found.')
        return post

    @Post.method(name='post.get', ########### FUNCIONA ############
                 request_fields=('id',),
                 path='getpost',
                 http_method='GET',
                 response_fields=('title','author_id','description','content','cover','date','tags','comments_all') ######## AHORA QUIERO QUE ADEMAS DEVUELVA LOS COMENTARIOS Y EL AUTOR COMPLETO DE CADA UNO #######
    )
    def get_post(self, post):
        if not post.from_datastore:
            raise endpoints.NotFoundException('Post not found.')
        return post

    @Post.query_method(name='post.list', ########## FUNCIONA ###########
                       path='post')
    def post_list(self, query):
        return query

    ################## COMMENT ##################
    @Comment.method(name='comment.insert', ########## FUNCIONA ###########
                    request_fields=('post_id','content'),
                    path='comment',
                    user_required=True,
                    response_fields=('post_id',)) ####### Devuelve el ID cuando se borro correctamente #######
    def insert_comment(self, comment):
        post = Post.get_by_id(comment.post_id)
        post.comments.append(Comment(content = comment.content, author = ndb.Key(Contributor, str(endpoints.get_current_user().email()))))
        post.put()
        return comment

    ################## EVENT ##################
    @Event.method(name="event.insert", ########## FUNCIONA ###########
                  request_fields=('id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid', 'sessions_id'),
                  path='event',
                  user_required=True)
    def insert_event(self, event):
        if event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s already exists.' % (name,))
        for session in event.sessions_id:
            event.sessions.append(ndb.Key(Session, str(session)))
        event.sessions_id = []
        event.put()
        return event

    @Event.method(name="event.add.sessions", ########## FUNCIONA ########### Aunque se puede repetir una misma Session, y no verifica si el ID de la Session realmente existe
                  request_fields=('id', 'sessions_id'),
                  path='event/add_sessions',
                  user_required=True)
    def add_sessions(self, event):
        if not event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s not exists.' % (name,))
        fullEvent = Event.get_by_id(event.id)
        for session in event.sessions_id:
            fullEvent.sessions.append(ndb.Key(Session, str(session)))
        fullEvent.put()
        return event

    @Event.method(name="event.remove.sessions", ########## FUNCIONA ###########
                  request_fields=('id', 'sessions_id'),
                  path='event/remove_sessions',
                  user_required=True)
    def remove_sessions(self, event):
        if not event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s not exists.' % (name,))
        fullEvent = Event.get_by_id(event.id)
        for session in event.sessions_id:
            fullEvent.sessions.remove(ndb.Key(Session, str(session)))
        fullEvent.put()
        return event

    @Event.method(name="event.remove.delete.sessions", ########## FUNCIONA ########### Hay que testearlo mejor
                  request_fields=('id', 'sessions_id'),
                  path='event/remove_and_delete_sessions',
                  user_required=True)
    def remove_sessions(self, event):
        if not event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s not exists.' % (name,))
        fullEvent = Event.get_by_id(event.id)
        for session in event.sessions_id:
            fullEvent.sessions.remove(ndb.Key(Session, str(session)))
            ndb.Key(Session, str(session)).delete()
        fullEvent.put()
        return event

    @Event.method(name='event.get', ########### FUNCIONA ############ Pero no devuelve las sesiones
                 request_fields=('id',),
                 path='event/get',
                 http_method='GET',
                 response_fields=('id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid', 'full_sessions')
    )
    def get_event(self, event):
        if not event.from_datastore:
            raise endpoints.NotFoundException('Event not found.')
        return event

    @Event.query_method(name="event.list", ########## FUNCIONA ###########
                        path="event")
    def event_list(self, query):
        return query

    ################## SESSION ##################
    @Session.method(name='session.insert', ########## FUNCIONA ###########
                    request_fields=('id', 'title', 'overview', 'startTime', 'endTime', 'contributors_id'),
                    path='session',
                    user_required=True)
    def insert_session(self, session):
        if session.from_datastore:
            name = session.key.string_id()
            raise endpoints.BadRequestException( 'Session of name %s already exists.' % (name,))
        for contributor in session.contributors_id:
            session.contributors.append(ndb.Key(Contributor, str(contributor)))
        session.contributors_id = []
        session.put()
        return session

application = endpoints.api_server([GDGMendozaAPI])

############ PARA VER SERVICIOS: /_ah/api/explorer
