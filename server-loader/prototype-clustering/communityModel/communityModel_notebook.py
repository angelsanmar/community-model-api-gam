
#--------------------------------------------------------------------------------------------------------------------------
#    Python libraries
#--------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import importlib

from inspect import getsourcefile
from os.path import abspath
import sys

#--------------------------------------------------------------------------------------------------------------------------
#    Custom Class
#--------------------------------------------------------------------------------------------------------------------------

from context import community_module
from dao.dao_json import DAO_json

from community_module.similarity.interactionSimilarityDAO import InteractionSimilarityDAO
from communityModel.communityJsonGenerator import CommunityJsonGenerator
from community_module.community_detection.explainedCommunitiesDetection import ExplainedCommunitiesDetection

# dao
from dao.dao_db_users import DAO_db_users
from dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from dao.dao_db_communities import DAO_db_community

from communityModel.communityModel import CommunityModel

#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunityModelNotebook(CommunityModel):
        
    def clustering(self, exportFile = "clustering.json"):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            percentageExplainability: minimum percentage of the most frequent value among 1+ main similarity features.
            
        """
        percentageExplainability = self.percentageExplainability
        
        # Initialize data
        algorithm = self.initializeAlgorithm()
        data = self.similarityMeasure.data
        data = data.set_index('userName')
        
        interactionObjectData = self.similarityMeasure.getInteractionObjectData()
        
        # Get results
        community_detection = ExplainedCommunitiesDetection(algorithm, data, self.distanceMatrix, self.perspective)
        communityDict = community_detection.search_all_communities(percentage=percentageExplainability) 
        communityDict['perspective'] = self.perspective
        
        # Export to json
        data.reset_index(inplace=True)
        exportFile = self.clusteringExportFileRoute(percentageExplainability)
        jsonGenerator = CommunityJsonGenerator(interactionObjectData, data, self.distanceMatrix, communityDict, community_detection, self.perspective)
        jsonCommunity = jsonGenerator.generateJSON(exportFile)       
        
        # Save data to database
        #self.saveDatabase(jsonCommunity)


        
        

        
    
    
    
    
    
    