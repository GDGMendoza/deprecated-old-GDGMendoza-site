'use strict';

var mongoose = require('mongoose'),
    Schema   = mongoose.Schema;

var sessionSchema = require('./sessionModel').schema;
var eventSchema = new Schema({
    title: { type: String, required: true, index: { unique: true } },
    description: { type: String },
    date: { type: Date },
    tags: [ { type: String } ],
    gmap: { type: String },
    flag: { type: String },
    gplus_eventid: { type: String },
    sessions: [ { type: sessionSchema } ]
});

var Event = mongoose.model('Event', eventSchema, 'EventModel');
module.exports = { model: Event, schema: eventSchema };