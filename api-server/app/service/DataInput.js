'use strict';
const db = require("../models");
var postData = require('./postData.js');

const InteractionData = db.interactionData;
const FlagDAO = db.flag;


/**
 * Redirects POST request to api_loader
 * Used to inform the community model about new perspectives 
 * 
 * body perspective object that will be added to the model
 * no response value expected for this operation
 */
exports.PostDataInput = function (body) {
    return new Promise(function (resolve, reject) {
        try {

            var json = { data: body }
            // save data
            InteractionData.insertData(json,
                data => {
                    resolve(data)
                },
                error => {
                    console.log("DataInput error2: " + error);
                    reject(error)
                })

            // var newBody = {
            //     perspectiveId: generatedId
            // }

            // post data to api_server.py
            // return postData.post_data(newBody, "/postData")
        } catch (error) {
            console.log("PostDataInput:" + error)
        }
    });
}

exports.getSeed = function () {
    return new Promise(function (resolve, reject) {

        //   let result = {};
        //   CommunityDAO.getById(communityId, 
        //     data => {
        //       result['application/json'] = data;
        //       if (Object.keys(result).length > 0) {
        //         resolve(result[Object.keys(result)[0]]);
        //       } else {
        //         resolve();
        //       }
        //     },
        //     error => {
        //       reject(error);
        //     }
        //   );    
    });
};