module.exports = mongoose => {
    var schema = mongoose.Schema(
      {
        data: mongoose.Mixed
      }
    );
  
    schema.method("toJSON", function () {
      const { __v, _id, ...object } = this.toObject();
      // object.id = _id.toString();
      return object;
    });
  
    const InteractionData = mongoose.model("InteractionData", schema);
  
    return {
      insertData: function (data, onSuccess, onError) {
        // console.log(json);
        InteractionData.create(data, function (err, res) {
          if (err) {
            console.log("insertData: error");
            onError(err);
          }
          else {
            onSuccess(res._id.toString());
          }
        });
      }
    };
  };
  
  