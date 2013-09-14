#  coding: utf-8 --
from api.lib import bottle
from api.lib.bottle import *
from api import blog, contributors, events
from api import poblate_script
# Si vamos a tener por separado los handlers, aca no deberiamos importar modelos :P
# from api.models import *

app = bottle.Bottle({'mode': 'development'})
response.content_type = 'application/json'

@app.route('/', method='GET')
def index():
    if 'MSIE' in request.headers['User-Agent']:
        return static_file('homeViewIE.html', root='./')
    else:
        return static_file('index.html', root='./')



## POSIBLES RETORNOS
    #return json_dumps(request.json) #devuelve los mismos parametros que llegaron por POST
    #request.json["nombre"] #sirve para leer el parametro nombre de POST
    #return bottle.json_dumps({"nombre": "pepe"}) #devuelve objeto json
    #return bottle.json_dumps([{"nombre": "pepe"},{"nombre": "honguito"}]) #devuelve array json

blog.initRoutes(app)
contributors.initRoutes(app)
events.initRoutes(app)
poblate_script.initRoutes(app)