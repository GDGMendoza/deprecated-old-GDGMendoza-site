
module.exports = function(app){

  require('./contributor')(app);
  require('./event')(app);
  require('./session')(app);
  require('./post')(app);

};