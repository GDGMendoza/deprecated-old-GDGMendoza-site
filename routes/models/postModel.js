'use strict';

var mongoose = require('mongoose'),
    Schema   = mongoose.Schema;

var commentsSchema = new Schema({
    author: { type: Schema.ObjectId, ref: 'Contributor' },
    content: { type: String },
    date: { type: Date, default: Date.now }
});
var postSchema = new Schema({
    title: { type: String, required: true, index: { unique: true } },
    author: { type: Schema.ObjectId, ref: 'Contributor' },
    description: { type: String },
    content: { type: String },
    cover: { type: String, required: true },
    date: { type: Date, default: Date.now },
    tags: [ { type: String } ],
    comments: [ { type: commentsSchema } ]
});

var Post = mongoose.model('Post', postSchema, 'PostModel');
module.exports = { model: Post, schema: postSchema };