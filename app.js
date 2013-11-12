
/**
 * Dependencias
 */

var http = require('http');
var path = require('path');
var express = require('express');
var mongoskin = require('mongoskin');
var app = express();
var db = mongoskin.db('mongodb://localhost/GDGMendoza', {safe:true});

//var routes = require('./routes');


/**
 * Configuración
 */

// Variables de entorno de session tanto para http como para socket
var cookieParser = express.cookieParser('dirtysecret');
var sessionStore = new express.session.MemoryStore({reapInterval: 5 * 60 * 1000});

// Configuración global
app.set('port', 3000);
app.use(express.favicon('public/favicon.ico'));
//app.use(express.logger('dev'));
app.use(express.urlencoded());
app.use(express.json());
app.use(express.methodOverride());
app.use(cookieParser);
app.use(express.session({store: sessionStore}));
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next();
});
app.use(express.static(path.join(__dirname, 'public')));
app.param('collectionName', function(req, res, next, collectionName){
  req.collection = db.collection(collectionName)
  return next()
})
//app.use(app.router);

// development only
if ('development' == app.get('env')) {
  //app.use(express.errorHandler());
}

// Referencias
var server = http.createServer(app);
//var io = require('socket.io').listen(server, { log: false });

//var SessionSockets = require('session.socket.io');
//var sessionSockets = new SessionSockets(io, sessionStore, cookieParser);


/**
 * Enrutamiento y Sockets
 */

require('./routes')(app);
//require('./routes/socket')(sessionSockets, io);


/**
 * Ejecución de servidor
 */

server.listen(app.get('port'), function () {
  console.log('Servidor Express iniciado en puerto ' + app.get('port'));
});
