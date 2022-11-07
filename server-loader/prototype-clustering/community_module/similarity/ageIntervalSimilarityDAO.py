# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from community_module.similarity.similarity import Similarity


HECHT_BELIEFS_R = ['ANatPridePro','BReligousPro','CRealisticPro','DExtremistNeg','EReligousNeg','FRealisticNeg']


class AgeIntervalSimilarityDAO(Similarity):

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
        return (abs(elemA - elemB))
        
        # """Overrides SimilarityFuntionInterface.computeSimilarity()"""
        # ageA = self.data.loc[self.data['userId'] == A]['age'].to_list()[0]
        # ageB = self.data.loc[self.data['userId'] == B]['age'].to_list()[0]
        # return (1 - (abs(ageA - ageB) / (self.age_index - 1)))
        
        
    def similarity(self,elemA, elemB):
        """Method to obtain the similarity between two element.

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
        return 1 - self.distance(elemA, elemB, numEmotions) # ¿No debería ser 1 / distancia?
        
        
        