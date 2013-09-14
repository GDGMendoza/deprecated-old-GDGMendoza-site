#  coding: utf-8 --
from api.lib import bottle
from api.lib.bottle import *
from api.models.post_model import Post, Comment
from json import dumps

def initRoutes(app=None):
    if not app:
        app = bottle.default_app()

    @app.route('/blog/getPostList', method='POST')  #testeado y andando!
    def getPostList():
        return Post.get_all_json()#[post.to_dict() for post in Post.query()]

    @app.route('/blog/getPost', method='POST')      #testeado y andando!
    def getPost():
        return Post.get_id_json(request.json["id"])

    @app.route('/put/post', method='POST')          #testeado y andando!
    def putPost():
        Post.put_post(
            id_query = request.json["id"],
            title = request.json["title"],
            author = request.json["author"],
            description = request.json["description"],
            content = request.json["content"],
            cover = request.json["cover"],
            tags = request.json["tags"]
        )
        return "Post agregado exitosamente!"

    @app.route('/edit/post', method='POST')          #testeado y andando (PD: CHAN por ahora es igual a put post)!
    def editPost():
        Post.put_post(
            id_query = request.json["id"],
            title = request.json["title"],
            author = request.json["author"],
            description = request.json["description"],
            content = request.json["content"],
            cover = request.json["cover"],
            tags = request.json["tags"]
        )
        return "Post editado exitosamente!"

    @app.route('/remove/post', method='POST')
    def removePost():                               #testeado y andando (PD: el metodo era delete, no remove)!
        Post.remove_post(request.json["id"])
        return "Post eliminado exitosamente!"

    @app.route('/put/comment', method='POST')
    def putComment():                               #testeado y andando!
        Comment.put_comment(
            id_query = request.json["data"]["id"],
            author = request.json["data"]["author"],        #IMPORTANTE, NUNCA SE DEBERÍA ESTAR LEYENDO COMO PARAMETRO ESTO!!! corregir ASAP!!
            content = request.json["data"]["content"]
        )
        return "Comentario agregado exitosamente!"