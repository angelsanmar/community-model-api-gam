# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarityDAO import SimilarityDAO


HECHT_BELIEFS_E = ['Justify','Balanced','Oppose']


class cosineSimilarityDAO(SimilarityDAO):

    def distance(self,elemA, elemB):
        
            
        #print(self.data)
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
        
        valueA = self.data.loc[elemA]['beliefE']
        valueB = self.data.loc[elemB]['beliefE']
        
        # Special case: dont know
        if (valueA == 'NoOpinion' and valueB == 'NoOpinion'):
            return 0
        #elif (elemA == 'NoOpinion' and elemB == 'Balanced'):
          #  return 0.25
        elif (valueA == 'NoOpinion' or valueB == 'NoOpinion'):
            return 0.5
        
        indexA = HECHT_BELIEFS_E.index(valueA)
        indexB = HECHT_BELIEFS_E.index(valueB)
        
        return (abs(indexA - indexB)) / (len(HECHT_BELIEFS_E) - 1)