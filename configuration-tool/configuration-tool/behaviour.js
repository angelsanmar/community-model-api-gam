const artworkAttDescription = {
  "artwork_attributes": [
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "Author",
          "att_type": "String"
        }
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "Description",
          "att_type": "String"
        }
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "Movement",
          "att_type": "String"
        }
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "Epoch",
          "att_type": "String"
        }
      }
    }
  ]
};

const citizenAttDescription = [
  {
    "att_name": "Age",
    "att_type": "String"
  },
  {
    "att_name": "Language",
    "att_type": "String"
  }
];

//http://localhost:8080/v1.1/perspective
function send(config = { "test": "test" }) {
  fetch("http://localhost:8080/v1.1/perspective", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(config)
  })
    .then(res => res.json())
    .then(function (res) {
      window.alert(res);
      window.alert(Object.keys(res));
    })
    .catch(function (err) {
      window.alert(err);
    });

}

const artwork_prefix = "artwork";
const user_prefix = "citizen";

document.addEventListener("DOMContentLoaded", function (event) {

  //http://localhost:8080/v1.1/seed
  // ./config.json
  // ./parser_output.json
  fetch("./parser_output.json") // Call the fetch function passing the url of the API as a parameter
    .then(configObj => configObj.json())
    .then(function (configObj) {
      // First, hide artwork attribute selection
      let artwork_attribs = document.getElementById("artwork-attribs");
      artwork_attribs.classList.add("hidden");

      // Hide/show artwork attribute selection depending on the word selected before "artwork"
      let artwork_sim = document.getElementById("similarity-2");
      artwork_sim.addEventListener("change", function () {
        let theValue = this.value;
        if (theValue === "similar") {
          artwork_attribs.classList.remove("hidden");
        } else {
          artwork_attribs.classList.add("hidden");
        }
      });

      // Create the artwork attribute selector for "similar" artworks
      let artworkAttDescriptionParsed = parseArtworkAttDescription(configObj.artwork_attributes);
      if (artworkAttDescriptionParsed.length > 0) {
        createAttributeSelector("artwork-attribs", artworkAttDescriptionParsed, artwork_prefix);
      }

      // Create and configure the citizen attribute selector
      createAttributeSelector("citizen-attribs", configObj.user_attributes, user_prefix);
      console.log(configObj)

      // Add form submit listener to create the new config file
      let form_config = document.getElementById("form-config");
      form_config.onsubmit = function (ev) {
        let newConfig = createConfigObjWithForm(ev, configObj);
        let theTextarea = document.getElementsByTagName("textarea")[0];
        theTextarea.value = JSON.stringify(newConfig, null, 4);
        theTextarea.style.height = (theTextarea.scrollHeight) + "px";
        // send(newConfig)
      }
    })
    .catch(function (err) {
      console.log(err)
      window.alert("Missing config.json");
    });
});

function createSelect(configObj) {
  for (const elem of attDescription) {
    const newElement = document.createElement('label');
    newElement.innerHTML = `<label><input type="checkbox" name="${prefix}-${elem.att_name}" value="${elem.att_name}" /> ${elem.att_name}</label>`;
    attributeContainer.appendChild(newElement);
  }

  let selectId = "similarity-1";
  var i = 0;
  for (const elem of select) {
    option = ""
    if (i == 0) {
      options += "<option selected>Select option</option>";
      i++;
    } else {
      options += "<option value=" + option + ">" + option + "</option>";
    }
  }
  document.getElementById("selectId").innerHTML = options;

  selectId = "similarity-object-1";
  i = 0;
  for (const elem of select) {
    option = ""
    if (i == 0) {
      options += "<option selected>Select option</option>";
      i++;
    } else {
      options += "<option value=" + option + ">" + option + "</option>";
    }
  }
  document.getElementById("selectId").innerHTML = options;

  selectId = "similarity-2";
  i = 0;
  for (const elem of select) {
    option = ""
    if (i == 0) {
      options += "<option selected>Select option</option>";
      i++;
    } else {
      options += "<option value=" + option + ">" + option + "</option>";
    }
  }
  document.getElementById("selectId").innerHTML = options;
}


/**
 * Create an attribute selector using a list of attribute descriptions
 * @param {string} containerId HTMl id (without #) of the attribute selector container 
 * @param {array}} attDescription  Array with attribute description object (with att_name and att_value keys)    
 */
function createAttributeSelector(containerId, attDescription, prefix) {
  let attributeContainer = document.querySelector("#" + containerId);

  for (const elem of attDescription) {
    const newElement = document.createElement('label');
    newElement.innerHTML = `<label><input type="checkbox" name="${prefix}-${elem.att_name}" value="${elem.att_name}" /> ${elem.att_name}</label>`;
    attributeContainer.appendChild(newElement);
  }
}

/**
 * Transform an object of artwork similarity functions in a list of attribute descripctions for @method createAttributeSelector
 * @param {object} artworkAttDescriptionObject An object that contains the description of the artwork similarity functions 
 * @returns A list with attribute descriptions
 */
function parseArtworkAttDescription(artworkAttDescriptionObject) {
  let result = [];
  for (const o of artworkAttDescriptionObject) {
    result.push(o.sim_function.on_attribute);
  }
  return result;
}

/**
 * Create a new configuration object using the form and the original configuration object 
 * @param {Event} ev Form event
 * @param {object} configObj Original config object to create the new one
 * @returns The new configuration object
 */
function createConfigObjWithForm(ev, configObj) {
  const newConfigObj = Object.assign({}, configObj);
  let form_config = document.getElementById("form-config");
  // Don't send data yet
  ev.preventDefault();

  // Create a new object (easier to manipulate)
  let theData = new FormData(form_config);
  let objData = {};
  for (const [key, value] of theData) {
    objData[key] = value;
  }

  // Which method is employed for emotion/values
  newConfigObj["interaction_similarity_functions"] = {
    "method": objData["sim-1"],
    "on": objData["sim-obj-1"],
  };

  // Update user attributes with the ones selected by the user
  let newUserAttributes = [];
  for (const att of configObj.user_attributes) {
    let key = `${user_prefix}-${att.att_name}`;
    if (key in objData) {
      newUserAttributes.push(att);
    }
  }
  newConfigObj.user_attributes = newUserAttributes;

  // Create a new objet to configure the artwork method because 
  // we need to add if they will be the same, similar or different
  newConfigObj["similarity_functions"] = {
    "method": objData["sim-2"],
    "artwork_attributes": [],
  };

  // Update artwork attributes if similar is selected
  let newArtworkAttributes = [];
  if (objData["sim-2"] === "similar") {
    for (const att of configObj.artwork_attributes) {
      let key = `${artwork_prefix}-${att.sim_function.on_attribute.att_name}`;
      if (key in objData) {
        newArtworkAttributes.push(att);
      }
    }
  }

  newConfigObj.similarity_functions.artwork_attributes = newArtworkAttributes;

  //Create name for the config file
  //   GAM SIM-E-SIM-A agglomerative (artist_country, iconclass)

  // SIM: similar
  // SA: Same
  // DIF: Different

  // E: Emotions
  // S: Sentiments

  // A: Artworks
  let configName = "GAM";
  let param;

  param = "sim-1";
  configName = configName + " ";
  if (objData[param] == "same")
    configName = configName + "SA";
  else if (objData[param] == "similar")
    configName = configName + "SIM";
  else if (objData[param] == "different")
    configName = configName + "DIF";

  param = "sim-obj-1";
  configName = configName + "-";
  if (objData[param] == "emotions")
    configName = configName + "E";
  else if (objData[param] == "sentiments")
    configName = configName + "S";

  param = "sim-2";
  configName = configName + "-";
  if (objData[param] == "same")
    configName = configName + "SA";
  else if (objData[param] == "similar")
    configName = configName + "SIM";
  else if (objData[param] == "different")
    configName = configName + "DIF";

  configName = configName + " A"; // Artwork
  configName = configName + " agglomerative"; // Artwork

  let artwork_attributesName = [];
  for (const att of configObj.artwork_attributes) {
    let key = `${artwork_prefix}-${att.sim_function.on_attribute.att_name}`;
    if (key in objData) {
      artwork_attributesName.push(att.sim_function.on_attribute.att_name);
    }
  }

  if (artwork_attributesName.length)
    configName = configName + " (" + artwork_attributesName.join(", ") + ")";

  console.log(configName);

  newConfigObj["fileName"] = configName;
  newConfigObj["fileId"] = configName;


  // Remove the old artwork_attributes object
  delete newConfigObj.artwork_attributes;

  return newConfigObj;
}