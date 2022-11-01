const PostDataInput = require('../service/DataInput.js');
var jobManager = require('./jobsRoute/jobsManager.js');


// redirect post request to api_loader
module.exports.postInputData = function postInputData(req, res, next) {
    try {
        // Gets current time, then converts it to number and then to base 36 ==> "l9x53lur"
        var generatedPerspectiveId = (+new Date).toString(36);
        PostDataInput.PostDataInput(generatedPerspectiveId, req.body)
            .then(function (response) {
                console.log(1)
                var data = jobManager.createJob(generatedPerspectiveId, "postDataInput")
                res.status(202).send(data);
            })
            .catch(function (response) {
                res.status(400).send("postInputData error");
                res.send(response);
            });
    } catch (error) {
        console.log("a")
        console.error(error)
        res.status(500)
        res.send(response);
    }
};