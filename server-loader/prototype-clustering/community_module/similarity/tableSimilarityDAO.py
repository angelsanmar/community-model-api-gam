# Authors: José Ángel Sánchez Martín

from community_module.similarity.similarityDAO import SimilarityDAO

import os
from inspect import getsourcefile
#from os.path import abspath, dirname


from context import dao
from dao.dao_csv import DAO_csv

class TableSimilarityDAO(SimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Construct of similarity objects for which the similarity values between items are given in a .csv

        Parameters
        ----------
        dao : dao_db_users class
            DAO which retrieves the user data
        similarityFunction: dict class including
            att_name: name of the attribute (column) the similarity measure is used upon
            weight: weight of the similarity measure
        """
        super().__init__(dao, similarityFunction)

        dao_csv = DAO_csv(os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) + "/distanceTables/" + self.similarityColumn + ".csv", ";")
        #print(dao_csv.getPandasDataframe())
        self.similarityTable = dao_csv.getPandasDataframe().set_index('Key')
        
    
    def distanceValues(self, valueA, valueB):
        """
        Method to obtain the distance between two valid values given by the similarity measure.
        e.g., sadness vs fear in plutchickEmotionSimilarity

        Parameters
        ----------
        valueA : object
            Value of first element corresponding to elemA in self.data
        valueB : object
            Value of first element corresponding to elemB in self.data

        Returns
        -------
        double
            Distance between the two values.
        """
        distance = self.similarityTable.loc[valueA][valueB]
        return distance
        
    