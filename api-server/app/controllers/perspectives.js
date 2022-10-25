const idParam = 'perspectiveId';
const Perspectives = require('../service/PerspectivesService.js');
const Flags = require('../service/FlagsService.js');
var post = require('./postUpdateCM');
var jobManager = require('./jobsRoute/jobsManager.js');

// check if flag exist
// if exist then update CM
// if !exist then access DB
module.exports.getPerspectives = function getPerspectives(req, res, next) {
  // Flags.getFlags()
  //   .then(function (response) {
  //     if (response == null) {
  Perspectives.getPerspectives()
    .then(function (response) {
      res.status(200).send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
  //   }
  //   else {
  //     post.update_CM("allPerspectives");
  //     var data = jobManager.createJob(0, "getPerspectives")
  //     res.status(202).send(data);
  //   }
  // })
  // .catch(function (response) {
  //   console.error("Perspectives.getPerspectives -> Flags.getFlags: error: " + response)
  // });
};

// check if flag exist
// if exist then update CM
// if !exist then access DB
module.exports.getPerspectiveById = function getPerspectiveById(req, res, next) {
  const perspectiveId = req.params[idParam];
  // Flags.getFlagsById(perspectiveId)
  //   .then(function (response) {
  //     if (response == null) {
  Perspectives.getPerspectiveById(perspectiveId)
    .then(function (response) {
      res.status(200).send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
  //   }
  //   else {
  //     post.update_CM(perspectiveId);
  //     var data = jobManager.createJob(0, "getPerspectives")
  //     res.status(202).send(data);
  //   }
  // })
  // .catch(function (response) {
  //   console.error("Perspectives.getPerspectiveById -> Flags.getFlagsById: error: " + response)
  // });
};

module.exports.listPerspectiveCommunities = function listPerspectiveCommunities(req, res, next) {
  const perspectiveId = req.params[idParam];

  // Check flag, if exist then access mongodb and return data
  // if false then check if perspetive exist, create new job and return 202, and a link to that job
  // Flags.getFlagsById(perspectiveId)
  //   .then(function (response) {
  //     if (response == null) { // flag does not exist => no update needed
  Perspectives.listPerspectiveCommunities(perspectiveId)
    .then(function (response) {
      res.status(200).send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
  //   }
  //   else { //flag exist
  //     post.update_CM(perspectiveId);
  //     var data = jobManager.createJob(perspectiveId, "listPerspectiveCommunities")
  //     res.status(202).send(data);
  //   }
  // })
  // .catch(function (response) {
  //   console.error("Perspectives.listPerspectiveCommunities -> Flags.getFlagsById: error: " + response)
  // });
};

// redirect post request to api_loader
module.exports.PostPerspective = function PostPerspective(req, res, next) {
  try {
    Perspectives.PostPerspective(req.body)
      .then(function (response) {
        res.status(204);
        res.send(response);
      })
      .catch(function (response) {
        res.status(501);
        res.send(response);
      });
  } catch (error) {
    console.error(error)
  }
};