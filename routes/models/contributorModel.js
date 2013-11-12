'use strict';

var mongoose = require('mongoose'),
    Schema   = mongoose.Schema;

var contributorSchema = new Schema({
    email: { type: String, required: true, index: { unique: true } },
    name: { type: String, required: true },
    job_position: { type: String },
    company: { type: String },
    google_plus: { type: String },
    facebook: { type: String },
    twitter: { type: String },
    access_level: { type: Number },
    description: { type: String },
    photo: { type: String },
    sessions: [ { type: Schema.ObjectId, ref: 'Session' } ],
    posts: [ { type: Schema.ObjectId, ref: 'Post' } ]
});

var Contributor = mongoose.model('Contributor', contributorSchema, 'ContributorModel');
module.exports = { model: Contributor, schema: contributorSchema };