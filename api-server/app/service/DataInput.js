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
        try {

            const http = require('http');
            // Sample URL

            const options = {
                // hostname: '172.20.0.4',
                host: '172.20.0.4',
                port: process.env.CM_DOCKER_PORT || 8090,
                path: "/seed",
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': 0,
                },
            };

            const request = http.request(options, (response) => {
                let data = '';
                response.on('data', (chunk) => {
                    data = data + chunk.toString();
                });

                response.on('end', () => {
                    const body = JSON.parse(data);
                    console.log(body);
                    resolve(body)
                });
            })

            request.on('error', (error) => {
                console.log('An error', error);
                reject(error)
            });

            request.end()
        } catch (error) {
            console.log(error)
            reject(error)
        }
    });
};