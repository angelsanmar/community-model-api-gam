import os

#--------------------------------------------------------------------------------------------------------------------------
#    Import
#--------------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import importlib
from context import community_module

# Community model tools
from communityModel.communityJsonGenerator import CommunityJsonGenerator

# clustering algorithms
from community_module.community_detection.explainedCommunitiesDetection import ExplainedCommunitiesDetection

# similarity measures
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO

# dao
from dao.dao_csv import DAO_csv
from dao.dao_db_users import DAO_db_users
from dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from dao.dao_db_communities import DAO_db_community

# json
#import json


#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunityModelOLD():

    def __init__(self,perspective,flag = {}):
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
        
    def start(self):
        self.similarityMeasure = self.initializeComplexSimilarityMeasure(DAO_db_users())
        self.distanceMatrix = self.computeDistanceMatrix()
        self.clustering(self.similarityMeasure)
    
    def initializeComplexSimilarityMeasure(self, dao):
        """
        Initializes the complex similarity measure associated to the given perspective

        Parameters
        ----------
        
        Returns
        -------
            similarityMeasure: ComplexSimilarityDAO
        """
        daoCommunityModel = dao
        similarityDict = self.perspective['similarity_functions']
        similarityMeasure = ComplexSimilarityDAO(daoCommunityModel,similarityDict)
        return similarityMeasure
    
    def computeDistanceMatrix(self):
        """
        Method to calculate the distance matrix between all elements included in data.

        Parameters
        ----------
        
        Returns
        -------
            distanceMatrix: np.ndarray
        """
        
        # Update distance matrix
        if (len(self.flag) > 0):
            # Load previous distance matrix
            daoDistanceMatrixes = DAO_db_distanceMatrixes()
            distanceMatrixJSON = daoDistanceMatrixes.getDistanceMatrix(self.perspective['id'])
            if (len(distanceMatrixJSON) == 0):
                distanceMatrix = np.empty([0,0])
            else:
                distanceMatrix = np.asarray(distanceMatrixJSON['distanceMatrix'])

            self.similarityMeasure.updateDistanceMatrix([self.flag['userid']], distanceMatrix)
        
        else:
            self.similarityMeasure.matrix_distance()
        
        # Drop irrelevant parameters to explain communities
        self.similarityMeasure.data.drop(['origin','source_id', '_id'], axis=1, inplace=True)
        self.similarityMeasure.data = self.similarityMeasure.data.rename(columns={"userid":"user"})
        
        return self.similarityMeasure.distanceMatrix
    
    # Only used for testing in jupyter notebook
    def setPerspective(self,perspective):
        self.perspective = perspective
            
    def clustering(self,similarityMeasure, exportFile = "", percentageDefaultParam = 0.5):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            
        """
        self.similarityMeasure = similarityMeasure
        self.exportFile = exportFile
        
        percentageDefault = percentageDefaultParam
        
        algorithmName = self.perspective['algorithm']['name'] + "CommunityDetection"
        algorithmFile = "community_module.community_detection." + algorithmName 
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(algorithmModule,algorithmName[0].upper() + algorithmName[1:])
        
        community_detection_df = similarityMeasure.data.set_index('userid')

        distanceMatrix = self.similarityMeasure.distanceMatrix
        community_detection = ExplainedCommunitiesDetection(algorithmClass, community_detection_df, distanceMatrix, self.perspective)

        n_communities, users_communities, self.medoids_communities = community_detection.search_all_communities(percentage=percentageDefault) 


        hecht_beliefR_pivot_df2 = community_detection_df.copy()
        hecht_beliefR_pivot_df2['community'] = users_communities.values()
        hecht_beliefR_pivot_df2.reset_index(inplace=True)
        hecht_beliefR_pivot_df2
        
        # Export to json
        self.exportCommunityClusteringJSON(hecht_beliefR_pivot_df2,community_detection,n_communities,percentageDefault,distanceMatrix)
        
#--------------------------------------------------------------------------------------------------------------------------
#    Complex similarity (HECHT) - Export JSON (with file)
#--------------------------------------------------------------------------------------------------------------------------

    def exportCommunityClusteringJSON(self, hecht_beliefR_pivot_df2,community_detection,n_communities,percentageDefault,distanceMatrix):
        # Group explicit community properties in one column
        json_df = hecht_beliefR_pivot_df2.copy()
        json_df['id'] = json_df['userid']
        json_df['label'] = json_df['userid']
        json_df = json_df.rename(columns={"community":"group"})
        columns = ['DemographicPolitics','DemographicReligous']
        columns = ['DemographicPolitics','DemographicReligous','beleifR','beliefJ']
        columns = self.perspective['user_attributes']
        json_df['explicit_community'] = json_df[columns].to_dict(orient='records')
        json_df


        # In[205]:


        jsonGenerator = CommunityJsonGenerator(json_df,community_detection,n_communities,percentageDefault,distanceMatrix,self.perspective['id'], self.medoids_communities)
        #jsonCommunity = jsonGenerator.generateJSON("../jsonVisualization/HECHT.json")

        #jsonCommunity = jsonGenerator.generateJSON("/app/prototype-clustering/examples/jsonVisualization/clustering.json")
        #jsonCommunity = jsonGenerator.generateJSON("/app/prototype-clustering/communityModel/jsonVisualization/clustering.json")       
        
        jsonCommunity = jsonGenerator.generateJSON(self.exportFile)       
        
        # Community jsons (visualization)
        #self.saveDatabase(jsonCommunity)
    

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
        
        
    
    
    
    
               
        
        
        
        

        
    
    
    