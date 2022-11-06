
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
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO


#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class ClusteringModel():

    def __init__(self,perspective):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspective: perspective object which includes artwork similarity information.
                similarity_functions: name, attribute, weight
        """
        self.perspective = perspective
        
    def initializeComplexSimilarityMeasure(self, dao):
        """
        Initializes the complex similarity measure associated to the given perspective

        Parameters
        ----------
        
        Returns
        -------
            similarityMeasure: ComplexSimilarityDAO
        """
        daoArtworkModel = dao
        self.similarityMeasure = ComplexSimilarityDAO(daoArtworkModel,self.perspective['similarity_functions'])
        return self.similarityMeasure       
        
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
        return self.distanceMatrix
    
    def saveDatabase(self):
        pass
        
        
        
    
    
    