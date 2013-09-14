#  coding: utf-8 --
from api.lib import bottle
from api.lib.bottle import *
from api.models.contributor_model import Contributor
from api.models.post_model import Comment, Post
# from api.models.event_model import Event
# from api.models.session_model import Session


def initRoutes(app=None):
    if not app:
        app = bottle.default_app()

    @app.route('/scripts/poblate', method='GET')
    def poblateDatastore():
        # Creamos los contributors
        hernan = Contributor(
            id='hermagrini',
            name='Hernán Magrini',
            photo='https://lh4.googleusercontent.com/-73rE-7CglS4/AAAAAAAAAAI/AAAAAAAABe0/k7B8LQJgma0/s120-c/photo.jpg',
            description='Hola Soy Hernán',
            email='her.magrini@gmail.com',
            gplus='http://gplus.to/hermagrini',
            fb='https://www.facebook.com/Her.Magrini',
            tw='https://twitter.com/hermagrini')
        hernan.put()
        heber = Contributor(
            id='heberlz',
            name='Heber López',
            photo='https://lh3.googleusercontent.com/-7gtLcVxZUhs/AAAAAAAAAAI/AAAAAAAABOY/ctEU3Dp4EHU/s120-c/photo.jpg',
            description='Hola Soy Heber',
            email='heberlopez@gmail.com',
            gplus='http://gplus.to/HeberLZ',
            fb='https://www.facebook.com/heberlopez',
            tw='https://twitter.com/heberlz')
        heber.put()
        tonga = Contributor(
            id='tonga298',
            name='Gastón Guidolín',
            photo='https://lh6.googleusercontent.com/--ZynD7DH-Zc/AAAAAAAAAAI/AAAAAAAAAbA/ragedlyYixc/s120-c/photo.jpg',
            description='Hola Soy Gastón',
            email='tonga.298@gmail.com',
            gplus='http://gplus.to/tonga298',
            fb='https://www.facebook.com/tonganomataras',
            tw='https://twitter.com/tonga298')
        tonga.put()
        cristian = Contributor(
            id='darkcause',
            name='Cristian Ríos',
            photo='https://lh4.googleusercontent.com/-EkSLBBbfffw/AAAAAAAAAAI/AAAAAAAAAFY/w8CTjlpLgjw/s120-c/photo.jpg',
            description='Hola Soy Cristian',
            email='matrixcmr@gmail.com',
            gplus='http://gplus.to/darkcause',
            fb='https://www.facebook.com/cristian.rios.darkcause',
            tw='https://twitter.com/xdarkcause')
        cristian.put()
        Post.put_post(
            id_query='post-con-titulo-by-hernan',
            title='post con titulo by hernan',
            author='hermagrini',
            description='whatever',
            content='sadsadsad',
            cover='http://us.123rf.com/400wm/400/400/pzaxe/pzaxe1108/pzaxe110800001/10113356-fondo-industrial-electronica-hi-tech-abstracto-verde-horizontal-vector.jpg',
            tags=['css','html']
        )
        Post.put_post(
            id_query='post-con-titulo-by-heber',
            title='post con titulo by heber',
            author='heberlz',
            description='whatever',
            content='sadsadsad',
            cover='https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSA2HVTlULB-Iur3LbsaOuslritMH_-zvXCQs3I704p-9NAC9A8',
            tags=['css','html']
        )
        Post.put_post(
            id_query='post-con-titulo-by-tonga',
            title='post con titulo by tonga',
            author='tonga298',
            description='whatever',
            content='sadsadsad',
            cover='http://blogs.salleurl.edu/cpd-tech-la-salle/files/2013/02/nano_tech-39440.jpeg',
            tags=['css','html']
        )
        Post.put_post(
            id_query='post-con-titulo-by-cristian',
            title='post con titulo by cristian',
            author='darkcause',
            description='tellmewhatyouwant',
            content='Porque un mago nunca llega tarde ni pronto, llega exactamente cuando se lo propone.',
            cover='http://www.fotos.org/galeria/data/900/impresionante-paisaje-fondos-de-pantalla.jpg',
            tags=['css','html']
        )
        return "Contributors & Posts Added Successfully"

