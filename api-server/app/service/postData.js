// postUpdateCM.js
// ========
/**
 * Sends a POST request to api_loader.py to update CM clustering 
 */

const http = require('http');

module.exports = {
    post_data: function (body, path) {
        var data = JSON.stringify(body)
        const options = {
            // hostname: '172.20.0.4',
            host: '172.20.0.4',
            port: process.env.CM_DOCKER_PORT || 8090,
            path: path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length,
            },
        };

        return new Promise((resolve, reject) => {
            const req = http.request(options, (res) => {
                res.on('data', (d) => {
                    process.stdout.write(d);
                });

                res.on('end', () => {
                    if (res.statusCode == 204) {
                        console.log('success')
                        resolve(body);
                    }
                    else {
                        console.log('failed')
                        resolve(body);
                    }
                });
                res.on('error', () => {
                    console.log('error');
                    reject(Error('HTTP call failed'));
                });
            });

            req.write(data);
            req.end();
        })
    }
};