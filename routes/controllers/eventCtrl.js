
var eventModel = require('../models/eventModel');

//User.find({}).populate('tasks').run(function(err, users) { //exec

var Event = {
    create: function(params, callback) {
        var newEvent = new eventModel.model({
            title: params.title,
            description: params.description,
            date: params.date,
            tags: params.tags,
            gmap: params.gmap,
            flag: params.flag,
            gplus_eventid: params.gplus_eventid,
            sessions: params.sessions
        });
        newEvent.save(function(err, event) {
            if(!err) {
                callback({ status: true, event: event });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    edit: function(params, callback) {
        eventModel.model.findByIdAndUpdate(params.id, {
            title: params.title,
            description: params.description,
            date: params.date,
            tags: params.tags,
            gmap: params.gmap,
            flag: params.flag,
            gplus_eventid: params.gplus_eventid,
            sessions: params.sessions
        }, function(err, event) {
            if(!err) {
                callback({ status: true, event: event });
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    get: function(params, callback){
        eventModel.model.findById(params.id, function(err, event) {
            if(!err) {
                if(event){
                    callback({ status: true, event: event });
                }else{
                    callback({ status: false });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    },
    list: function(params, callback) {
        eventModel.model.find({}, function(err, events) {
            if(!err) {
                callback({ response: true, events: events });
            } else {
                callback({ response: null, err: err });
            }
        });
    },
    del: function(params, callback) {
        eventModel.model.findById(params.id, function(err, event) {
            if(!err) {
                if(event){
                    event.remove();
                    callback({ status: true });
                }
            } else {
                callback({ status: null, err: err });
            }
        });
    }
};

module.exports = Event;