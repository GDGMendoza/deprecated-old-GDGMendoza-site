
var sessionModel = require('../models/sessionModel');

//User.find({}).populate('tasks').run(function(err, users) { //exec

var Session = {
    create: function(params, callback) {
        var newSession = new sessionModel.model({
            title: params.title,
            overview: params.overview,
            startTime: params.startTime,
            endTime: params.endTime,
            contributors: params.contributors
        });
        newSession.save(function(err, session) {
            if(!err) {
                callback({ status: true, session: session });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    edit: function(params, callback) {
        sessionModel.model.findByIdAndUpdate(params.id, {
            title: params.title,
            overview: params.overview,
            startTime: params.startTime,
            endTime: params.endTime,
            contributors: params.contributors
        }, function(err, session) {
            if(!err) {
                callback({ status: true, session: session });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    get: function(params, callback){
        sessionModel.model.findById(params.id, function(err, session) {
            if(!err) {
                if(session){
                    callback({ status: true, session: session });
                }else{
                    callback({ status: false });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    list: function(params, callback) {
        sessionModel.model.find({}, function(err, sessions) {
            if(!err) {
                callback({ response: true, sessions: sessions });
            } else {
                callback({ response: null, err: err });
            }
        });
    },
    del: function(params, callback) {
        sessionModel.model.findById(params.id, function(err, session) {
            if(!err) {
                if(session){
                    session.remove();
                    callback({ status: true });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    }
};

module.exports = Session;