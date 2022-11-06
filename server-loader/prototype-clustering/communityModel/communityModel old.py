
#--------------------------------------------------------------------------------------------------------------------------
#    Python libraries
#--------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import importlib

#--------------------------------------------------------------------------------------------------------------------------
#    Custom Class
#--------------------------------------------------------------------------------------------------------------------------

from context import community_module
from dao.dao_json import DAO_json

from community_module.similarity.interactionSimilarityDAO import InteractionSimilarityDAO
from communityModel.communityJsonGenerator import CommunityJsonGenerator
from community_module.community_detection.explainedCommunitiesDetection import ExplainedCommunitiesDetection

#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunityModel():

    def __init__(self,perspective,flag = {}, daoRoute = 'data/processed/GAM user_interactions.json'):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspective: perspective object. Composed by:
                id, name
                algorithm: name and parameters
                similarity_functions: name, attribute, weight
            flag: flag object. Composed by:
                perspectiveId
                userid: user to update
        """
        self.perspective = perspective
        self.flag = flag
        self.daoRoute = daoRoute
  
    def start(self):
        """
        Compute community model
        
        a) Initialize similarity measures. 
            1) "interaction_similarity_functions" is empty: normal computation of similarity using sim_functions with complexSimilarityDAO
            2) "interaction_similarity_functions" is not empty: interactionSimilarityDAO is initialized. It sets a ComplexSimilarityDAO por the interactive object (e.g., artwork)
            and another one for the interaction attributes.
        b) Computes distance matrix between main attributes.
        c) Performs clustering
        Parameters
        ----------

        """
        self.initializeSimilarityMeasure()

        self.computeDistanceMatrix()   
        
        self.clustering()
        
    def initializeSimilarityMeasure(self, daoRoute = 'data/processed/GAM user_interactions.json'):
        daoJson = DAO_json(self.daoRoute)
        self.similarityMeasure = InteractionSimilarityDAO(daoJson, self.perspective)
        
    def computeDistanceMatrix(self):
        """
        Method to calculate the distance matrix between all elements included in data.

        Parameters
        ----------
        
        Returns
        -------
            distanceMatrix: np.ndarray
        """
        #self.similarityMeasure.distance(2,10)
        
        # import it
        distanceMatrixFileRoute = "distanceMatrix/" + self.perspective['name'] + ".json"
        file_exists = os.path.exists(distanceMatrixFileRoute)
        if file_exists and 1 == 2:
            print("distance matrix clustering file exists")
            self.distanceMatrix = self.similarityMeasure.importDistanceMatrix(distanceMatrixFileRoute)
        else:
            print("distance matrix clustering file doesnt exist")
            self.distanceMatrix = self.similarityMeasure.matrix_distance()
            self.similarityMeasure.exportDistanceMatrix(self.distanceMatrix, distanceMatrixFileRoute)
    
        return self.distanceMatrix
        
    def clustering(self, percentageExplainability = 0.5, exportFile = "clustering.json"):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            percentageExplainability: minimum percentage of the most frequent value among 1+ main similarity features.
            
        """
        # Initialize data
        algorithm = self.initializeAlgorithm()
        data = self.similarityMeasure.data
        data = data.set_index('userName')
        
        interactionObjectData = self.similarityMeasure.getInteractionObjectData()
        
        print(self.distanceMatrix)
        
        print("algorithm: " + str(algorithm))
        
        # Get results
        community_detection = ExplainedCommunitiesDetection(algorithm, data, self.distanceMatrix, self.perspective)
        communityDict = community_detection.search_all_communities(percentage=percentageExplainability) 
        communityDict['perspective'] = self.perspective
        
        # Export to json
        data.reset_index(inplace=True)
        exportFile = "clustering/" + self.perspective['name'] + " " + "(" + self.perspective['algorithm']['name'] + ")" 
        exportFile += " (" + str(percentageExplainability) + ")"
        exportFile += ".json"
        jsonGenerator = CommunityJsonGenerator(interactionObjectData, data, self.distanceMatrix, communityDict, community_detection, self.perspective)
        jsonCommunity = jsonGenerator.generateJSON(exportFile)       
        
        # Save data to database
        # self.saveDatabase(jsonCommunity)

    def initializeAlgorithm(self):
        algorithmName = self.perspective['algorithm']['name'] + "CommunityDetection"
        algorithmFile = "community_module.community_detection." + algorithmName 
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(algorithmModule,algorithmName[0].upper() + algorithmName[1:])
        
        return algorithmClass
        

#--------------------------------------------------------------------------------------------------------------------------
#    Community jsons (visualization)
#--------------------------------------------------------------------------------------------------------------------------

    def saveDatabase(self,jsonCommunity):
        """
        daoCommunityModelVisualization = DAO_visualization()
        daoCommunityModelVisualization.drop()
        daoCommunityModelVisualization.insertJSON(jsonCommunity)
        """
        
        # Store distance matrix data
        # https://pynative.com/python-serialize-numpy-ndarray-into-json/
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        #daoDistanceMatrixes.drop()
        daoDistanceMatrixes.updateDistanceMatrix({'perspectiveId': self.perspective['id'], 'distanceMatrix': self.similarityMeasure.distanceMatrix.tolist()})
        
        # Store community data
        daoCommunityModelCommunity = DAO_db_community()
        # drop previous data
        daoCommunityModelCommunity.drop({'perspectiveId': self.perspective['id']})
        daoCommunityModelCommunity.dropFullList({'perspectiveId': self.perspective['id']})
        #daoCommunityModelCommunity.dropFullList()
        # add new data
        daoCommunityModelCommunity.insertFileList("", jsonCommunity)
        
        
    
    
    
    
               
        
        
        
        

        
    
    
    
    
    
    