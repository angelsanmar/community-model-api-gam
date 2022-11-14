# Authors: José Ángel Sánchez Martín
from community_module.similarity.similarityDAO import SimilarityDAO

class IntersectionSimilarityDAO(SimilarityDAO):

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
        
        # Get string separated by ,
        valueA = self.data.loc[elemA][self.similarityColumn]
        valueB = self.data.loc[elemB][self.similarityColumn]
        
        # Convert to list
        listA = valueA.split(", ")
        listB = valueB.split(", ")
        listA = list(filter(None, listA))
        listB = list(filter(None, listB))

        # sets
        setA = set(listA)
        setB = set(listB)
        
        # Get intersection
        intersection = setA.intersection(setB)
        union = setA.union(setB)
        
        # Similarity = size intersection / size union
        return 1 - (len(intersection) / len(union))
        