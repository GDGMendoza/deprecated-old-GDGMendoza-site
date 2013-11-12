'use strict';

var mongoose = require('mongoose'),
    Schema   = mongoose.Schema;

var sessionSchema = new Schema({
    title: { type: String },
    overview: { type: String },
    startTime: { type: String },
    endTime: { type: String },
    contributors: [ { type: Schema.ObjectId, ref: 'Contributor' } ]
});

var Session = mongoose.model('Session', sessionSchema, 'SessionModel');
module.exports = { model: Session, schema: sessionSchema };