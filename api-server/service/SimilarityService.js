'use strict';


/**
 * Dissimilarity between two communities
 * Returns the dissimilarity score between two communities
 *
 * communityId Long ID of the target community to compute dissimilarity
 * otherCommunityId Long ID of the other community to compute dissimilarity
 * returns similarityScore
 **/
exports.computeDissimilarity = function(communityId,otherCommunityId) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
}, {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * K-most dissimilar communities
 * Returns a list with the k most dissimilar communities to the chosen one in the model.
 *
 * communityId Long ID of the target community to compute dissimilarity
 * k Integer Size of the result (k most dissimilar communities)
 * returns similarityScore
 **/
exports.computeKmostDissimilar = function(communityId,k) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
}, {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * K-most similar communities
 * Returns a list with the k most similar communities to the chosen one in the model.
 *
 * communityId Long ID of the target community to compute similarity
 * k Integer Size of the result (k most similar communities)
 * returns similarityScore
 **/
exports.computeKmostSimilar = function(communityId,k) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
}, {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Similarity between two communities
 * Returns a similarity score between two communities.
 *
 * communityId Long ID of the target community to compute similarity
 * otherCommunityId Long ID of the other community to compute similarity
 * returns similarityScore
 **/
exports.computeSimilarity = function(communityId,otherCommunityId) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
}, {
  "target-community-id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "similarity-function" : "similarity-function",
  "value" : 0.8008281904610115
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}
