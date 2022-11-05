'use strict';
const db = require("../models");
var postData = require('./postData.js');

const PerspectiveDAO = db.perspectives;
const CommunityDAO = db.communities;
const FlagDAO = db.flag;


/**
* Perspectives in the model
* Access to a list of the Perspectives
*
* returns List
**/
exports.getPerspectives = function () {
  return new Promise(function (resolve, reject) {

    let result = {};
    PerspectiveDAO.all((perspectives) => {
      result['application/json'] = perspectives;
      if (Object.keys(result).length > 0) {
        resolve(result[Object.keys(result)[0]]);
      } else {
        resolve();
      }
    });
  });

};


/**
* Returns information about a perspective
*
* perspectiveId Long ID of perspective to return
* returns perspective
**/
exports.getPerspectiveById = function (perspectiveId) {
  return new Promise(function (resolve, reject) {

    let result = {};
    PerspectiveDAO.getById(perspectiveId,
      data => {
        // console.log(data)
        result['application/json'] = data;
        if (Object.keys(result).length > 0) {
          resolve(result[Object.keys(result)[0]]);
        } else {
          resolve();
        }
      },
      error => {
        reject(error);
      }
    );
  });
};


/**
* Returns list with communities that have the same perspectiveId
*
* perspectiveId Long ID of perspective 
* returns List
**/
exports.listPerspectiveCommunities = function (perspectiveId) {
  return new Promise(function (resolve, reject) {
    // obtains all communities and then filter them by perspectiveId
    let result = {};
    let data = []
    let communities = {};
    CommunityDAO.all((com) => {
      communities = com;
      if (communities.length == 0) {
        resolve();
      }

      for (var i = 0; i < communities.length; i++) {
        var community = communities[i]
        if (community.perspectiveId == perspectiveId) {
          data.push(community);
        }
      }
      // communities.forEach(element => {
      //   var community = JSON.parse(element);
      //   console.log(community);
      //   if (community.perspective == perspectiveId) {
      //     data.push(communities);
      //   }
      // });

      result['application/json'] = data;
      if (Object.keys(result).length > 0) {
        resolve(result[Object.keys(result)[0]]);
      } else {
        resolve();
      }
    });

  });
};


const http = require('http');

/**
 * Redirects POST request to api_loader
 * Used to inform the community model about new perspectives 
 * 
 * body perspective object that will be added to the model
 * no response value expected for this operation
 */
exports.PostPerspective = function (body, generatedId) {
  // return new Promise(function (resolve, reject) {
  try {
    var json = {
      perspectiveId: generatedId,
      data: body
    };

    // create flag
    FlagDAO.insertFlag(json,
      data => {
        // resolve(data)
      },
      error => {
        console.log("FlagDAO.insertFlag error1: " + error);
        // reject(error)
      })

    var json2 = body
    json2["perspectiveId"] = generatedId

  } catch (error) {
    console.log(error)
  }
  return postData.post_data(json2, "/perspective")
  // });
}