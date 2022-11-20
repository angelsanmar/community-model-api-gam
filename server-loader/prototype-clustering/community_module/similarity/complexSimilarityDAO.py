# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math



from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_BELIEFS_R = ['ANatPridePro','BReligousPro','CRealisticPro','DExtremistNeg','EReligousNeg','FRealisticNeg']

class ComplexSimilarityDAO(SimilarityDAO):

    def __init__(self,dao,similarity_functions):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao to obtain data from database
        similarityDict: dictionary
            Dictionary with keys (similarity measure classes) and values (weight of that similarity measure)
        
        """
        super().__init__(dao)
        
        # similarity_functions
        self.similarityDict = {}
        for similarityFunction in similarity_functions:
            similarityMeasure = self.initializeFromPerspective(dao,similarityFunction)
            #self.similarityDict[similarityMeasure] = similarityFunction['sim_function']['weight']
            self.similarityDict[similarityMeasure] = similarityFunction['sim_function']
        
        
    def distance(self,elemA, elemB):
        """Method to obtain the distance between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """
        complexDistance = 0
        complexWeight = 0
        for similarity, similarityFunction in self.similarityDict.items():
            weight = similarityFunction.get('weight',0.5)
            
            simDistance = similarity.distance(elemA,elemB)
            simDistance = similarity.dissimilarFlag(simDistance)
            simDistance2 = simDistance * weight
            
            complexDistance += simDistance2
            complexWeight = complexWeight + weight 

        complexDistance = complexDistance / complexWeight
        
        return complexDistance
        

        