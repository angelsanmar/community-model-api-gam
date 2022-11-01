'use strict';
const db = require("../models");
var postData = require('./postData.js');

const PerspectiveDAO = db.perspectives;
const CommunityDAO = db.communities;
const FlagDAO = db.flag;


/**
 * Redirects POST request to api_loader
 * Used to inform the community model about new perspectives 
 * 
 * body perspective object that will be added to the model
 * no response value expected for this operation
 */
exports.PostDataInput = function (generatedId, body) {
    // return new Promise(function (resolve, reject) {
    // try {
    var json = {
        perspectiveId: generatedId,
        data: body
    };
    FlagDAO.insertFlag(json,
        data => {
            // resolve(data)
        },
        error => {
            console.log("DataInput error: " + error);
            // reject(error)
        })

    var newBody = {
        perspectiveId: generatedId
    }

    return postData.post_data(newBody, "/postData")
    // } catch (error) {
    //     console.log(error)
    // }
    // });
}