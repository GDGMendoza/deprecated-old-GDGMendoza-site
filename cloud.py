# -*- coding: utf-8 -*-
from google.appengine.ext import endpoints
from protorpc import remote

from api.lib.custom_handler import improve
import json

##################### MODELS ########################
from api.models_cloud.post_model import Post, Comment
from api.models_cloud.contributor_model import Contributor
from api.models_cloud.event_model import Session, Event

################################################ CLOUD ENDPOINTS SERVICE  ##############################################
@endpoints.api(name='gdgmendoza', version='v1',
               description='API for GDG Mendoza Management')
class GDGMendozaAPI(remote.Service):
    ############## CONTRIBUTOR ################
  @Contributor.method(name='contributor.insert', ########### FUNCIONA ############
               path='contributor')
  def insert_contributor(self, contributor):
    contributor.put()
    return contributor

  @Contributor.query_method(name='contributor.list', ########### FUNCIONA ############
                     path='contributor')
  def contributor_list(self, query):
    return query

  ################## POST #####################
  @Post.method(name='post.insert', ########### FUNCIONA ############ Pero no agrega al author
               path='post/{id}')
  def insert_post(self, post):
      if post.from_datastore:
          name = post.key.string_id()
          raise endpoints.BadRequestException( 'Post of name %s already exists.' % (name,))
      post.put()
      return post

  @Post.method(name='post.delete', ########### FUNCIONA ############
               path='deletepost/{id}',
               response_fields=('id',)) ####### Devuelve el ID cuando se borro correctamente #######
  def delete_post(self, post):
      if post.from_datastore:
          Post.remove_post(post.id)
      else:
          raise endpoints.NotFoundException('Post not found.')
      return post

  @Post.method(name='post.get', ########### FUNCIONA ############
               request_fields=('id',),
                 path='getpost/{id}',
                 http_method='GET',
                 response_fields=('title','author','autorcompleto','description','content','cover','date','tags','comentarioscompleto') ######## AHORA QUIERO QUE ADEMAS DEVUELVA LOS COMENTARIOS Y EL AUTOR COMPLETO DE CADA UNO #######
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
  #@Post.method(name='comment.insert',
  #                path='post/{id}')
  #def insert_comment(self, post):
  #    # Hipoteticamente hablando... debería de seleccionar el post y despues appendear el comentario pero... que se yo jajaja
  #    return post

application = endpoints.api_server([GDGMendozaAPI])

############ PARA VER SERVICIOS: /_ah/api/explorer
