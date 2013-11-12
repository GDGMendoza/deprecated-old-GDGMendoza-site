
var postModel = require('../models/postModel');

//User.find({}).populate('tasks').run(function(err, users) { //exec

var Post = {
    create: function(params, callback) {
        var newPost = new postModel.model({
            title: params.title,
            author: params.author,
            description: params.description,
            content: params.content,
            cover: params.cover,
            tags: params.tags
        });
        newPost.save(function(err, post) {
            if(!err) {
                callback({ status: true, post: post });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    edit: function(params, callback) {
        postModel.model.findByIdAndUpdate(params.id, {
            title: params.title,
            author: params.author,
            description: params.description,
            content: params.content,
            cover: params.cover,
            tags: params.tags
        }, function(err, post) {
            if(!err) {
                callback({ status: true, post: post });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    get: function(params, callback){
        postModel.model.findById(params.id, function(err, post) {
            if(!err) {
                if(post){
                    callback({ status: true, post: post });
                }else{
                    callback({ status: false });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    list: function(params, callback) {
        postModel.model.find({}, function(err, posts) {
            if(!err) {
                callback({ response: true, posts: posts });
            } else {
                callback({ response: null, err: err });
            }
        });
    },
    del: function(params, callback) {
        postModel.model.findById(params.id, function(err, post) {
            if(!err) {
                if(post){
                    post.remove();
                    callback({ status: true });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    comment: function(params, callback) {
        postModel.model.findByIdAndUpdate(params.id, {
            $push: { comments: params.comment }
        }, function(err, post) {
            if(!err) {
                callback({ status: true, post: post });
            } else {
                callback({ status: null, err: err });
            }
        });
    }
};

module.exports = Post;