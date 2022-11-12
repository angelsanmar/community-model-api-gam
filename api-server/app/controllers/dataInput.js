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
    res.status(200).send(getExampleSeed());
    // DataInput.getSeed()
    //     .then(function (response) {
    //         var seed = response
    //         res.status(200).send(seed);
    //     })
    //     .catch(function (response) {
    //         res.status(400).send("seed error");
    //     });
};


function getExampleSeed() {
    let seed = {
        "artwork_attributes": [
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Inventary",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Collection",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Author",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Year",
                        "att_type": "Number"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Artwork_start_date",
                        "att_type": "Number"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Gender",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Artist_country",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "taxonomySimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Artwork_Artistic_Movement",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "taxonomySimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Technique",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "taxonomySimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Artwork_type",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Size_height",
                        "att_type": "Number"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "equalSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Size_width",
                        "att_type": "Number"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "taxonomySimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Materials",
                        "att_type": "String"
                    }
                }
            },
            {
                "sim_function": {
                    "name": "taxonomySimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "Iconclass_subjects_curators",
                        "att_type": "String"
                    }
                }
            }
        ],
        "user_attributes": [
            {
                "att_name": "Age",
                "att_type": "String"
            },
            {
                "att_name": "Gender",
                "att_type": "String"
            },
            {
                "att_name": "relationship_with_arts",
                "att_type": "String"
            },
            {
                "att_name": "relationship_with_museums",
                "att_type": "String"
            }
        ],
        "interaction_similarity_functions": [
            {
                "sim_function": {
                    "name": "emotionSimilarity",
                    "params": [],
                    "on_attribute": {
                        "att_name": "emotions",
                        "att_type": "String"
                    },
                    "interaction_object": {
                        "att_name": "artworkId",
                        "att_type": "String"
                    }
                }
            }
        ]
    };
    return seed;
}