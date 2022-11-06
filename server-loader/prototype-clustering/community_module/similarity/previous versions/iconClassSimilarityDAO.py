# Authors: José Ángel Sánchez Martín

import networkx as nx
from community_module.similarity.similarityDAO import SimilarityDAO
from community_module.similarity.taxonomies.taxonomy import Taxonomy

import os

class IconClassSimilarityDAO(SimilarityDAO):
    
    def __init__(self, dao, similarityFunction):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao)
        self.similarityColumn = similarityFunction['on_attribute']['att_name']
        
        #self.taxonomy = Taxonomy(self.data.columns.name)
        
    def getGraph():
        return self.taxonomy.getGraph()

    def elemLayer(self,elem):
        return len(elem)
    
    def taxonomyDistance(self,elemA,elemB):
        """Method to obtain the distance between two taxonomy members.

        Parameters
        ----------
        elemA : object
            Id of first element. This id should be in self.data.
        elemB : object
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Similarity between the two taxonomy members.
        """
        commonAncestor = os.path.commonprefix([elemA, elemB])
        print(elemA)
        print(elemB)
        print(commonAncestor)
        sim = self.elemLayer(commonAncestor) / max(self.elemLayer(elemA), self.elemLayer(elemB))
        print(self.elemLayer(elemA))
        print(self.elemLayer(elemB))
        print(self.elemLayer(commonAncestor))
        return 1 - sim

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
        
        # Get first common characters 
        # https://stackoverflow.com/questions/18715688/find-common-substring-between-two-strings
        valueA = self.data.loc[elemA][self.similarityColumn]
        valueB = self.data.loc[elemB][self.similarityColumn]
        
        valueA = valueA.split("; ")[0]
        valueB = valueB.split("; ")[0]
                
        return self.taxonomyDistance(valueA.split(" ")[0],valueB.split(" ")[0])
        
        #return 1 - self.similarity(elemA,elemB)

    
    
    
    
    
    
    
    
    