module.exports = mongoose => {
    var schema = mongoose.Schema(
        {
            id: String,
            perspectiveId: String
        }
    );

    schema.method("toJSON", function () {
        const { __v, _id, ...object } = this.toObject();
        // object.id = _id.toString();
        return object;
    });

    const CommunitiesVis = mongoose.model("communitiesVisualization", schema, "communitiesVisualization");

    // Access mongobd and retrieve requested data
    return {
        getById: function (id, onSuccess, onError) {
            CommunitiesVis.findOne({ perspectiveId: id }, { projection: { _id: 0 } }, function (error, data) {
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
