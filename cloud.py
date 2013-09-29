# -*- coding: utf-8 -*-
from google.appengine.ext import endpoints
from protorpc import remote
from google.appengine.ext import ndb

#https://gist.github.com/aseemk/4461785 ESTÁNDARES

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

    @Contributor.method(name='contributor.edit', ########### FUNCIONA ############
                        path='contributor/{id}',
                        request_fields=('id', 'name', 'job_position', 'company', 'google_plus', 'facebook', 'twitter', 'description', 'photo'),
                        user_required=True,
                        response_fields=('id',))
    def edit_contributor(self, contributor):
        if not contributor.from_datastore:
            raise endpoints.BadRequestException( 'User %s does not exists.' % (contributor.id,))
        if contributor.id != endpoints.get_current_user().email(): #para que no pisen el id al ejecutarse el set_id
            raise endpoints.BadRequestException( 'Invalid user')
        contributor.put()
        return contributor

    @Contributor.query_method(name='contributor.list', ########### FUNCIONA ############
                              path='contributor')
    def contributor_list(self, query):
        return query

    @Contributor.method(name='contributor.get', ########### FUNCIONA ############
                 request_fields=('id',),
                 path='contributor/{id}',
                 http_method='GET')
    def get_contributor(self, contributor):
        if not contributor.from_datastore:
            raise endpoints.NotFoundException('Contributor not found.')
        return contributor

    @Contributor.method(name='contributor.delete', ########### FUNCIONA ############
                 path='contributor/{id}',
                 http_method='DELETE',
                 request_fields=('id',),
                 response_fields=('id',),
                 user_required=True) ####### Devuelve el ID cuando se borro correctamente #######
    def delete_contributor(self, contributor):
        if contributor.id != endpoints.get_current_user().email(): # Para que no borren la cuenta de alguien mas
            raise endpoints.BadRequestException( 'Invalid user')
        if contributor.from_datastore:
            ndb.Key("Contributor", contributor.id).delete()
        else:
            raise endpoints.NotFoundException('Contributor not found.')
        return contributor



    ################## EVENT ##################
    @Event.method(name="event.insert", ########## FUNCIONA ###########
                  request_fields=('id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid', 'sessions_id'),
                  response_fields=('id',),
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

    @Event.method(name="event.edit", ########## FUNCIONA ###########
                  request_fields=('id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid'),
                  response_fields=('id',),
                  path='event/{id}',
                  user_required=True)
    def edit_event(self, event):
        if not event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s does not exists.' % (name,))
        event.put()
        return event

    @Event.method(name='event.get', ########### FUNCIONA ############ Pero no devuelve las sesiones
                 request_fields=('id',),
                 path='event/{id}',
                 http_method='GET',
                 response_fields=('id', 'title', 'description', 'date', 'tags', 'gmap', 'flag', 'gplus_eventid', 'full_sessions')
    )
    def get_event(self, event):
        if not event.from_datastore:
            raise endpoints.BadRequestException('Event not found.')
        return event

    @Event.query_method(name="event.list", ########## FUNCIONA ###########
                        path="event")
    def event_list(self, query):
        return query

    @Event.method(name='event.delete', ########### FUNCIONA ############
                 path='event/{id}',
                 http_method='DELETE',
                 request_fields=('id',),
                 response_fields=('id',),
                 user_required=True) ####### Devuelve el ID cuando se borro correctamente #######
    def delete_event(self, event):
        if event.from_datastore:
            ndb.Key("Event", event.id).delete()
        else:
            raise endpoints.BadRequestException('Event not found.')
        return event

    @Event.method(name="event.add_sessions", ########## FUNCIONA ########### Testear si funciona que no se repita
                  request_fields=('id', 'sessions_id'),
                  response_fields=('id',),
                  path='event/{id}/add_sessions',
                  user_required=True)
    def add_sessions(self, event):
        if not event.from_datastore:
            name = event.key.string_id()
            raise endpoints.BadRequestException( 'Event of name %s not exists.' % (name,))
        fullEvent = Event.get_by_id(event.id)
        for session in event.sessions_id:
            aux = ndb.Key(Session, str(session))
            if aux not in fullEvent.sessions:
                fullEvent.sessions.append(aux)
        fullEvent.put()
        return event

    @Event.method(name="event.remove_sessions", ########## FUNCIONA ###########
                  request_fields=('id', 'sessions_id'),
                  response_fields=('id',),
                  path='event/{id}/remove_sessions',
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

    ################## SESSION ##################
    @Session.method(name='session.insert', ########## FUNCIONA ###########
                    request_fields=('id', 'title', 'overview', 'startTime', 'endTime', 'contributors_id'),
                    response_fields=('id',),
                    path='session/{id}',
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

    @Session.method(name="session.edit",
                  request_fields=('id', 'title', 'overview', 'startTime', 'endTime', 'contributors_id'),
                  response_fields=('id',),
                  path='session/{id}',
                  user_required=True)
    def edit_session(self, session):
        if not session.from_datastore:
            name = session.key.string_id()
            raise endpoints.BadRequestException( 'Session of name %s does not exists.' % (name,))
        session.put()
        return session

    @Session.method(name='session.get',
                 request_fields=('id',),
                 path='session/{id}',
                 http_method='GET',
                 user_required=True)
    def get_session(self, session):
        if not session.from_datastore:
            raise endpoints.BadRequestException('Session not found.')
        return session

    @Session.query_method(name="session.list",
                        path="session",
                        user_required=True)
    def session_list(self, query):
        return query

    @Session.method(name='session.delete',
                 path='session/{id}',
                 http_method='DELETE',
                 request_fields=('id',),
                 response_fields=('id',),
                 user_required=True) ####### Devuelve el ID cuando se borro correctamente #######
    def delete_session(self, session):
        if session.from_datastore:
            ndb.Key("Session", session.id).delete()
        else:
            raise endpoints.BadRequestException('Session not found.')
        return session


# DE ACA EN ADELANTE POROBOMBOMBOM CAJAAAAAAAAAAAA CAJAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA HOLA

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
                 path='get/post',
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

############ PARA VER SERVICIOS: /_ah/api/explorer

application = endpoints.api_server([GDGMendozaAPI])

