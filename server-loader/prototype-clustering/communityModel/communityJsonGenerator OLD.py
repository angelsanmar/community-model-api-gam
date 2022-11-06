import pandas as pd
import numpy as np

import json
import math
"""
86ca1aa0-34aa-4e8b-a509-50c905bae2a2
86ca1aa0-34aa-4e8b-a509-50c905bae2a2
"""
class CommunityJsonGenerator:

    def __init__(self, data, communityDetection, n_communities, percentageDefault, distanceMatrix, perspectiveId, medoids_communities, answer_binary=False, skipPropertyValue = False):
        self.json_df = data
        self.community_detection = communityDetection
        self.n_communities = n_communities
        self.medoids_communities = medoids_communities
        self.percentageDefault = percentageDefault
        self.distanceMatrix = distanceMatrix
        self.perspectiveId = perspectiveId
        self.answerBinary = answer_binary
        self.skipPropertyValue = skipPropertyValue
        
    
    def generateJSON(self,filename):
        # Export community information to JSON format
        self.communityJson = {}
        
        self.communityJSON()
        self.userJSON()
        self.similarityJSON()
        
        print("\n\n")
        print("generate json " + filename)
        print(self.communityJson)
        print("\n\n")
        
        
        with open(filename, "w") as outfile:
            json.dump(self.communityJson, outfile, indent=4)
        """
        """
        
        return self.communityJson
        
    def communityJSON(self):
        # Community Data
        self.communityJson['perspectiveId'] = self.perspectiveId
        self.communityJson['numberOfCommunities'] = 0
        self.communityJson['communities'] = []


        for c in range(self.n_communities):
            community_data = self.community_detection.get_community(c, answer_binary=self.answerBinary, percentage=self.percentageDefault)
            
            print("\n")
            print("json generator")
            print(self.medoids_communities[c])
            
            communityDictionary = {}
            communityDictionary['id'] = self.perspectiveId + "-" + str(c)
            communityDictionary['perspectiveId'] = self.perspectiveId
            communityDictionary['community-type'] = 'implicit'
            communityDictionary['name'] = 'Community ' + str(c)
            communityDictionary['medoid'] = self.medoids_communities[c]
            
            # communityDictionary['representative'] = self.medoids_communities[c].iloc[0]['user']
            
            if len(community_data['members']) > 1:
                communityPropertiesList = []
                for k in community_data['explanation'][0].keys():
                    #print('\t\t-', k)
                    #communityProperties += '\t\t-' + ' ' + str(k) + ' ' + community_data['properties'][k] + '\n'

                    if (self.skipPropertyValue):
                        communityPropertiesList.append("'" + str(k) + "'")
                    else:
                        communityPropertiesList.append("'" + str(k) + "'"  + ': ' + "'" + str(community_data['explanation'][0][k]) + "'")
                
                #communityProperties = 'Similar dominant emotions while interacting with the following artworks: {'
                #communityProperties = 'Artworks the community members interacted with: {'
                communityProperties = 'Minimum percentage of users with the representative properties: ' + community_data['percentage'] + "; "
                communityProperties += 'Representative Properties: {'
                
                communityProperties += '; '.join(communityPropertiesList)
                communityProperties += '}'
                
            else:
                communityProperties = 'Users without community'
                
            communityDictionary['explanation'] = []
            communityDictionary['explanation'].append(communityProperties)
            
            # UNCOMMENT THIS WHEN IT WORKS WITH JUPYTER NOTEBOOK
            #communityDictionary['explanation'].append(community_data['explanation'][1])
            
            
            #communityDictionary[name]['users'] = 
            
            
            communityDictionary['users'] = []
            for user in community_data['members']:
                communityDictionary['users'].append(str(user))
            
            #print(communityDictionary)
            self.communityJson['communities'].append(communityDictionary)
          
        self.communityJson['numberOfCommunities'] = len(self.communityJson['communities'])
            
    def userJSON(self):
        # User Data
        self.communityJson["users"] = []
        self.communityJson['users'] = self.json_df[['id','label','group','explicit_community']].to_dict('records')
        #self.communityJson
    
    def similarityJSON(self):
        # Similarity Data
        self.communityJson['similarity'] = []    
        # users
        for i in range(len(self.distanceMatrix)):
            for j in range(i+1,len(self.distanceMatrix[i])):
                dicti = {}
                dicti['u1'] = str(self.json_df.iloc[i]['label'])
                dicti['u2'] = str(self.json_df.iloc[j]['label'])
                #dicti['value'] = similarityMatrix[i][j]
                dicti['value'] = round(1 - self.distanceMatrix[i][j],2)
                self.communityJson['similarity'].append(dicti)           
                    
            
            
            
            
            