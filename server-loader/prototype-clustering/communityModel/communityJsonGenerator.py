import pandas as pd
import numpy as np

import json
import math

import uuid
"""
86ca1aa0-34aa-4e8b-a509-50c905bae2a2
86ca1aa0-34aa-4e8b-a509-50c905bae2a2
"""

import re


class CommunityJsonGenerator:

    def __init__(self, interactionObjectData, data, distanceMatrix, communityDict, community_detection, perspective):
        self.io_df = interactionObjectData
        self.json_df = data.copy()
        self.distanceMatrix = distanceMatrix
        self.communityDict = communityDict
        self.community_detection = community_detection
        self.perspective = perspective
        
        # Adapt self.json_df
        #print(self.json_df)
        self.json_df['id'] = self.json_df['userName']
        self.json_df['label'] = self.json_df['userName']
        self.json_df['group'] = communityDict['users'].values()
        self.json_df['explicit_community'] = self.json_df[communityDict['userAttributes']].to_dict(orient='records')
        #self.generateUserInteractionColumnMaster()
        self.generateUserInteractionColumn()
        
        # Extra to make it work with Marco Visualization
        self.io_df['Year'] = self.io_df['Year'].astype(str)
        
        self.io_df.rename(columns = {'_id':'id'}, inplace = True)
        self.io_df.rename(columns = {'Title':'tittle'}, inplace = True)
        self.io_df.rename(columns = {'Author':'author'}, inplace = True)
        self.io_df.rename(columns = {'Year':'year'}, inplace = True)
        self.io_df.rename(columns = {'Link':'image'}, inplace = True)
        
        
    
    def generateDict(self, element):
        # return {'IdArtefact': element[0], 'emotions': element[1]} 
        # return {'artwork_id': str(element[0]), 'feelings': "scettico", 'extracted_emotions': element[1]} 
        return {'artwork_id': str(element[0]), 'feelings': element[2], 'extracted_emotions': element[1]} 
        
        #return {
    
    def generateUserInteractionColumnMaster(self):
        # Get IO_attributes
        IO_id = self.perspective['interaction_similarity_functions'][0]['sim_function']['interaction_object']['att_name']
        IO_similarityFeatures = [IO_id]
        for similarity_function in self.perspective['interaction_similarity_functions']:
            IO_similarityFeature = similarity_function['sim_function']['on_attribute']['att_name']
            IO_similarityFeatures.append(IO_similarityFeature)
            
        # https://stackoverflow.com/questions/34066053/from-list-of-dictionaries-to-np-array-of-arrays-and-vice-versa
        # https://stackoverflow.com/questions/8372399/zip-with-list-output-instead-of-tuple
        # Testing 2
        json_df2 = self.json_df[IO_similarityFeatures].head(2)
        IO_columnList = []
        for i in list(json_df2):
            IO_columnList.append(json_df2[i].tolist())
        user_interactions = [list(a) for a in zip(*IO_columnList)]
        
        """
        print("user_interactions: " + str(user_interactions))
        print("\n\n\n")
        """
        
        """
        for i in list(json_df2):
        
        list1 = json_df2['IdArtefact', 'sentiment'].tolist()
        print("List1: " + str(list1))
            
        """   
            
            
        # Testing
        json_df2 = self.json_df.head(2)
        print("testing")
        print(json_df2[IO_id])
        print(json_df2[IO_similarityFeatures])
        print("\n")
        print(json_df2[IO_similarityFeatures].values[0][0])
        print("\n\n\n")
        
        list1 = [[1,2],[3,4],[5,6]]
        result = list(zip(*list1))
        print("result: " + str(result))
        
        list1 = json_df2[IO_similarityFeatures].values
        list1 = [json_df2['IdArtefact'], json_df2['sentiment']]
        print("List1: " + str(list1))
        result = list(zip(*list1))
        print("result: " + str(result))
        
        json_df3 = json_df2.copy()
        json_df3['interactions'] = zip(*json_df2[IO_similarityFeatures])
        print("json_df3")
        print(json_df3['interactions'])
        print("\n\n\n")
            
        # Generate user_interactions
        user_interactions = self.json_df.apply(lambda row: type(row), axis = 1)
        print(user_interactions)
        
        #user_interactions = self.json_df.apply(lambda row: list(map(self.generateDict, list(zip(row[IO_id], row['emotions'])))), axis = 1)
        self.json_df['interactions'] = user_interactions
        
        
    def generateUserInteractionColumn(self):
        # Get interaction columns
        IO_id = self.perspective['interaction_similarity_functions'][0]['sim_function']['interaction_object']['att_name']
        IO_similarityFeatures = []
        for similarity_function in self.perspective['interaction_similarity_functions']:
            IO_similarityFeature = similarity_function['sim_function']['on_attribute']['att_name']
            IO_similarityFeatures.append(IO_similarityFeature)
                                                           
        # Generate interaction info column
        IO_columns = []
        IO_columns.append(IO_id)
        IO_columns.extend(IO_similarityFeatures)
        print("IO_columns: " + str(IO_columns))
            
        user_interactions = self.json_df.apply(lambda row: list(map(self.generateDict, list(zip(row[IO_id], row[IO_similarityFeatures[0]], row['ItMakesMeFeel'])))), axis = 1)
        #user_interactions = self.json_df.apply(lambda row: list(map(self.generateDict, list(zip(row[IO_id], row['emotions'])))), axis = 1)
        
        self.json_df['interactions'] = user_interactions
        
        
        """
        user_df3 = json_df2.apply(lambda row: {key: value for key, value in zip(row)}, axis = 1)
        print("user_df3")
        print(user_df3)
        print("\n")
        """
        
        """
        # https://stackoverflow.com/questions/48011404/pandas-how-to-combine-multiple-columns-into-an-array-column
        user_interactions = self.json_df[['IdArtefact','emotions']].head(3).values.tolist()
        print(user_interactions)
        """
        
        
        """
        user_interactions = self.json_df[['IdArtefact','emotions']].apply(lambda row: list({stocks: prices for stocks,
            prices in zip(row)}), axis=1)
        
        
        print("user_interactions")
        print(self.json_df[['IdArtefact','emotions']].head(2))
        print("\n")
        print(user_interactions.head(2))
        """
       
        
        
        
    def generateJSON(self,filename):
        # Export community information to JSON format
        self.communityJson = {}
        
        self.communityJSON()
        self.userJSON()
        self.similarityJSON()
        self.interactionObjectJSON()
        
        """
        self.communityJson['fileId'] = str(uuid.uuid1())
        self.communityJson['fileName'] = self.communityDict['perspective']['name']
        """
        
        # Remove parts to work with Marco visualization
        #self.communityJson.pop('perspectiveId')
        #self.communityJson.pop('numberOfCommunities')
        #self.communityJson['communities'].pop('community-type')
        #self.communityJson['communities'].pop('medoid')
        
        print("\n\n")
        print("generate json " + filename)
        #print(self.communityJson)
        print("\n\n")
        
        
        with open(filename, "w") as outfile:
            json.dump(self.communityJson, outfile, indent=4)
        """
        """
        
        return self.communityJson
        
    def communityJSON(self):
        self.skipPropertyValue = False
        
        
        # Community Data
        self.communityJson['name'] = self.communityDict['perspective']['name']
        self.communityJson['perspectiveId'] = self.communityDict['perspective']['id']
        #self.communityJson['numberOfCommunities'] = self.communityDict['number']
        self.communityJson['communities'] = []
        
        self.implicitExplanationJSON()
        
    def implicitExplanationJSON(self):
        # Users without community
        usersWithoutCommunity = []
        
        for c in range(self.communityDict['number']):
            community_data = self.community_detection.get_community(c, answer_binary=False, percentage=self.communityDict['percentage'])
            
            # Check if the community is a valid one (more than one member); otherwise the only member doesn't have a community
            if len(community_data['members']) > 1:
                # basic information
                communityDictionary = {}
                communityDictionary['id'] = self.communityDict['perspective']['id'] + "-" + str(len(self.communityJson['communities']))
                communityDictionary['perspectiveId'] = self.communityDict['perspective']['id']
                communityDictionary['community-type'] = 'implicit'
                communityDictionary['name'] = 'Community ' + str(len(self.communityJson['communities']))
            
                # Explanations
                communityDictionary['explanations'] = []
            
                # medoid
                medoidJson = {'medoid': self.communityDict['medoids'][c]}
                medoidJson = {'explanation_type': 'medoid', 'explanation_data': {'id': self.communityDict['medoids'][c]}, 'visible': True}
                communityDictionary['explanations'].append(medoidJson)
            
                # Implicit community explanation
                implicitPropertyExplanations = {}
                
                for key in community_data['explanation'].keys():
                    #print('\t\t-', k)
                    #communityProperties += '\t\t-' + ' ' + str(k) + ' ' + community_data['properties'][k] + '\n'
                    
                    communityPropertiesDict = {}

                    if (self.skipPropertyValue):
                        communityPropertiesList.append("'" + str(k) + "'")
                    else:
                        #communityPropertiesList.append("'" + str(k) + "'"  + ': ' + "'" + str(community_data['explanation'][0][k]) + "'")
                        #communityPropertiesList.append(community_data['explanation'][0][k])
                        
                        
                        keyValueList = community_data['explanation'][key].split("\n")
                        print("keyValueList: " + str(keyValueList))
                        for keyValue in keyValueList:
                            pattern = r'\W+'
                            # empty character " " one or more times
                            pattern = r'\s+'
                            #keyValueSplit = keyValue.split("    ")
                            keyValueSplit = re.split(pattern, keyValue)
                            key2 = keyValueSplit[0]
                            value = keyValueSplit[1]
                            value = float(value)
                            communityPropertiesDict[key2] = value
                        
                        implicitPropertyExplanations[key] = communityPropertiesDict
                
                
                # Implicit attribute (explanation)
                for implicitAttribute in implicitPropertyExplanations.keys():
                
                    explanationJson = {}
                    explanationJson['explanation_type'] = 'implicit_attributes'
                    explanationJson['explanation_data'] = {}
                    
                    explanationJson['explanation_data']['label'] = 'Percentage distribution of the implicit attribute ' + "(" + implicitAttribute + ")" + ":"
                    explanationJson['explanation_data']['data'] = implicitPropertyExplanations[implicitAttribute]

                    explanationJson['visible'] = True
                    
                    communityDictionary['explanations'].append(explanationJson)
                

                # Explicit attributes (explanation)
                explanationJson = {}
                explanationJson['explanation_type'] = 'explicit_attributes'
                explanationJson['explanation_data'] = {}
                explanationJson['visible'] = True
                
                communityDictionary['explanations'].append(explanationJson)

                # Get members
                communityDictionary['users'] = []
                communityDictionary['users'] = community_data['members']
                    
                # add it to communities
                self.communityJson['communities'].append(communityDictionary)
                
                # Update the group to which the users belong
                self.json_df.loc[ self.json_df['id'].isin(community_data['members']), 'group'] = len(self.communityJson['communities']) - 1
                    
            else:
                usersWithoutCommunity.extend(community_data['members'])
        
        self.communityJson['numberOfCommunities'] = len(self.communityJson['communities'])
        
        # Add users without community
        if (len(usersWithoutCommunity) > 0):
            communityJson = {}
            communityJson['id'] = self.communityDict['perspective']['id'] + "-" + str(len(self.communityJson['communities'])) + ' (Users without community)'
            communityJson['perspectiveId'] = self.communityDict['perspective']['id']
            communityJson['community-type'] = 'inexistent'
            communityJson['name'] = 'Community ' + str(len(self.communityJson['communities'])) + ' (Users without community)'
            communityJson['explanations'] = []
            communityJson['users'] = usersWithoutCommunity
            
            self.communityJson['communities'].append(communityJson)
        
        # Update the group value for the users not belonging to any community
        self.json_df.loc[ self.json_df['id'].isin(usersWithoutCommunity), 'group'] = len(self.communityJson['communities']) - 1
      




      
            
    def userJSON(self):
        # User Data
        self.communityJson["users"] = []
        self.communityJson['users'] = self.json_df[['id','label','group','explicit_community','interactions']].to_dict('records')
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
                    
    def interactionObjectJSON(self):
        # https://www.leocon.dev/blog/2021/09/how-to-flatten-a-python-list-array-and-which-one-should-you-use/
        # self.io_df2 = self.io_df.filter(regex = '^(?!.*timestamp).*$')
        # key = 'IdArtefact'
        #key = 'artworkId'
        key = self.perspective['interaction_similarity_functions'][0]['sim_function']['interaction_object']['att_name']
        
        """
        print("interaction object json part")
        print("key: " + str(key))
        """


        
        interactedIO = self.json_df[key].tolist()
        interactedIO = list(sum(interactedIO, []))
        interactedIO = list(map(str, interactedIO))
        
        # @id is for ints
        io_df2 = self.io_df[self.io_df['id'].isin(interactedIO)]
        self.communityJson['artworks'] = io_df2.to_dict('records')
        

        
    
            
            
            
            