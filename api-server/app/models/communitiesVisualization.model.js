module.exports = mongoose => {
    var schema = mongoose.Schema(
        {
            id: String,
            fileId: String,
            communities: [{
                _id: false,
                "community-type": String,
                perspectiveId: String,
                name: String,
                explanation: String,
                users: [String]
            }],
            users: [{
                _id: false,
                "userid": String,
                "origin": String,
                "source_id": String,
                "source": String,
                "pname": String,
                "pvalue": String,
                "context": String,
                "datapoints": Number
            }],
            similarity: [{
                _id: false,
                "target-community-id": String,
                "other-community-id": String,
                "similarity-function": String,
                value: Number
            }],

        }
    );

    schema.method("toJSON", function () {
        const { __v, _id, ...object } = this.toObject();
        // object.id = _id.toString();
        return object;
    });

    /**
     * http://localhost:8080/visualizationAPI/file/{fileId}
     */

    const CommunitiesVis = mongoose.model("communitiesVisualization", schema, "communitiesVisualization");

    // Access mongobd and retrieve requested data
    return {
        getById: function (id, onSuccess, onError) {
            CommunitiesVis.findOne({ fileId: id }, { projection: { _id: 0 } }, function (error, data) {
                if (error) {
                    onError(error);
                } else {
                    if (data) {
                        console.log(data)
                        onSuccess(data.toJSON());
                    }
                    else {
                        onError("file with that id does not exist");
                    }
                }
            });

        }
    };
};
