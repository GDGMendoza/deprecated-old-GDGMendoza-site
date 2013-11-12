
module.exports = function(app){

    var sessionCtrl = require('./controllers/sessionCtrl');

	app.post('/api/session', function(req, res){
        sessionCtrl.create({
            title: req.body.title,
            overview: req.body.overview,
            startTime: req.body.startTime,
            endTime: req.body.endTime,
            contributors: req.body.contributors
        }, function(response){
            res.json(response);
        });
		console.log('Session insertado');
	});
	app.put('/api/session/:id', function(req,res){
        sessionCtrl.edit({
            id: req.params.id,
            title: req.body.title,
            overview: req.body.overview,
            startTime: req.body.startTime,
            endTime: req.body.endTime,
            contributors: req.body.contributors
        }, function(response){
            res.json(response);
        });
		console.log('Session editado');
	});
	app.get('/api/session', function(req,res){
        sessionCtrl.list({}, function(response){
            res.json(response);
        });
		console.log('Session listado devuelto');
	});
	app.get('/api/session/:id', function(req,res){
        sessionCtrl.get({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Session devuelto');
	});
	app.del('/api/session/:id', function(req,res){
        sessionCtrl.del({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Session eliminado');
	});
};