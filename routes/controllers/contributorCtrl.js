
var contributorModel = require('../models/contributorModel');

//User.find({}).populate('tasks').run(function(err, users) { //exec

var Contributor = {
    create: function(params, callback) {
        var newContributor = new contributorModel.model({
            email: params.email,
            name: params.name,
            job_position: params.job_position,
            company: params.company,
            google_plus: params.google_plus,
            facebook: params.facebook,
            twitter: params.twitter,
            access_level: 0,
            description: params.description,
            photo: params.photo
        });
        newContributor.save(function(err, contributor) {
            if(!err) {
                callback({ status: true, contributor: contributor });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    edit: function(params, callback) {
        contributorModel.model.findByIdAndUpdate(params.id, {
            email: params.email,
            name: params.name,
            job_position: params.job_position,
            company: params.company,
            google_plus: params.google_plus,
            facebook: params.facebook,
            twitter: params.twitter,
            description: params.description,
            photo: params.photo,
            sessions: params.sessions,
            posts: params.posts
        }, function(err, contributor) {
            if(!err) {
                callback({ status: true, contributor: contributor });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    get: function(params, callback){
        contributorModel.model.findById(params.id, function(err, contributor) {
            if(!err) {
                if(contributor){
                    callback({ status: true, contributor: contributor });
                }else{
                    callback({ status: false });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    list: function(params, callback) {
        contributorModel.model.find({}, function(err, contributors) {
            if(!err) {
                callback({ response: true, contributors: contributors });
            } else {
                callback({ response: null, err: err });
            }
        });
    },
    del: function(params, callback) {
        contributorModel.model.findById(params.id, function(err, contributor) {
            if(!err) {
                if(contributor){
                    contributor.remove();
                    callback({ status: true });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    }
};

module.exports = Contributor;