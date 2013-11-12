
module.exports = function(app){

    var postCtrl = require('./controllers/postCtrl');

	app.post('/api/post', function(req, res){
        postCtrl.create({
            title: req.body.title,
            author: req.body.author,
            description: req.body.description,
            content: req.body.content,
            cover: req.body.cover,
            tags: req.body.tags
        }, function(response){
            res.json(response);
        });
		console.log('Post insertado');	
	});
	app.put('/api/post/:id', function(req,res){
        postCtrl.edit({
            id: req.params.id,
            title: req.body.title,
            author: req.body.author,
            description: req.body.description,
            content: req.body.content,
            cover: req.body.cover,
            tags: req.body.tags
        }, function(response){
            res.json(response);
        });
		console.log('Post editado');
	});
	app.get('/api/post', function(req,res){
        postCtrl.list({}, function(response){
            res.json(response);
        });
		console.log('Post listado devuelto');
	});
	app.get('/api/post/:id', function(req,res){
        postCtrl.get({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Post devuelto');
	});
	app.del('/api/post/:id', function(req,res){
        postCtrl.del({ id: req.params.id }, function(response){
            res.json(response);
        });
		console.log('Post eliminado');
	});

	app.post('/api/post/:id/comment', function(req, res){
        postCtrl.comment({
            id: req.params.id,
            comment: req.body.comment
        }, function(response){
            res.json(response);
        });
		console.log('Post comentario insertado');
	});
};