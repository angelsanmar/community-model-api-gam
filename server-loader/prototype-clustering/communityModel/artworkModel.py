
#--------------------------------------------------------------------------------------------------------------------------
#    Python libraries
#--------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np

#--------------------------------------------------------------------------------------------------------------------------
#    Custom Class
#--------------------------------------------------------------------------------------------------------------------------

from context import community_module
from dao.dao_json import DAO_json

from communityModel.clusteringModel import ClusteringModel
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO


#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class ArtworkModel(ClusteringModel):
  
    def start(self):
        daoJson = DAO_json('data/GAM_Catalogue_plus.json')
        self.similarityMeasure = self.initializeComplexSimilarityMeasure(daoJson)
        
        self.computeDistanceMatrix()       
        
    def computeDistanceMatrix(self):
        """
        Method to calculate the distance matrix between all elements included in data.

        Parameters
        ----------
        
        Returns
        -------
            distanceMatrix: np.ndarray
        """
        self.distanceMatrix = self.similarityMeasure.matrix_distance()
        print(self.distanceMatrix)
        return self.distanceMatrix
    
    def saveDatabase(self):
        pass
        
        
        
    
    
    