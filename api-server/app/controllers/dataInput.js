const DataInput = require('../service/DataInput.js');
var jobManager = require('./jobsRoute/jobsManager.js');


// redirect post request to api_loader
module.exports.postInputData = function postInputData(req, res, next) {
    try {

        DataInput.PostDataInput(req.body)
            .then(function (response) {
                res.status(200).send(response);
            })
            .catch(function (response) {
                res.status(400).send("postInputData error");
                res.send(response);
            });
    } catch (error) {
        console.error("postInputData:" + error)
        res.status(500)
    }
};

module.exports.getSeed = function getSeed(req, res, next) {
    DataInput.getSeed()
        .then(function (response) {
            var seed = response
            res.status(200).send(seed);
        })
        .catch(function (response) {
            res.status(400).send("seed error");
        });
};