
module.exports = function(app){

    var eventCtrl = require('./controllers/eventCtrl');

	app.post('/api/event', function(req, res){
        eventCtrl.create({
            title: req.body.title,
            description: req.body.description,
            date: req.body.date,
            tags: req.body.tags,
            gmap: req.body.gmap,
            flag: req.body.flag,
            gplus_eventid: req.body.gplus_eventid,
            sessions: req.body.sessions
        }, function(response){
            res.json(response);
        });
		console.log('Event insertado');
	});
	app.put('/api/event/:id', function(req,res){
        eventCtrl.edit({
            id: req.params.id,
            title: req.body.title,
            description: req.body.description,
            date: req.body.date,
            tags: req.body.tags,
            gmap: req.body.gmap,
            flag: req.body.flag,
            gplus_eventid: req.body.gplus_eventid,
            sessions: req.body.sessions
        }, function(response){
            res.json(response);
        });
		console.log('Event editado');
	});
	app.get('/api/event', function(req,res){
        eventCtrl.list({}, function(response){
            res.json(response);
        });
		console.log('Event listado devuelto');
	});
	app.get('/api/event/:id', function(req,res){
        eventCtrl.get({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Event devuelto');
	});
	app.del('/api/event/:id', function(req,res){
        eventCtrl.del({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Event eliminado');
	});
	
};