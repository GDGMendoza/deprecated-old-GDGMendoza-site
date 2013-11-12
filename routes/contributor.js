
module.exports = function(app){

    var contributorCtrl = require('./controllers/contributorCtrl');

	app.post('/api/contributor', function(req, res){
        contributorCtrl.create({
            email: req.body.email,
            name: req.body.name,
            job_position: req.body.job_position,
            company: req.body.company,
            google_plus: req.body.google_plus,
            facebook: req.body.facebook,
            twitter: req.body.twitter,
            description: req.body.description,
            photo: req.body.photo
        }, function(response){
            res.json(response);
        });
		console.log('Contributor insertado');
	});
	app.put('/api/contributor/:id', function(req,res){
        contributorCtrl.edit({
            id: req.params.id,
            email: req.body.email,
            name: req.body.name,
            job_position: req.body.job_position,
            company: req.body.company,
            google_plus: req.body.google_plus,
            facebook: req.body.facebook,
            twitter: req.body.twitter,
            description: req.body.description,
            photo: req.body.photo,
            sessions: req.body.sessions,
            posts: req.body.posts
        }, function(response){
            res.json(response);
        });
		console.log('Contributor editado');
	});
	app.get('/api/contributor', function(req,res){
        contributorCtrl.list({}, function(response){
            res.json(response);
        });
		console.log('Contributor listado devuelto');
	});
	app.get('/api/contributor/:id', function(req,res){
        contributorCtrl.get({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Contributor devuelto');
	});
	app.del('/api/contributor/:id', function(req,res){
        contributorCtrl.del({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Contributor eliminado');
	});
};