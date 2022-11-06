# Authors: José Ángel Sánchez Martín
import os
from community_module.similarity.similarityDAO import SimilarityDAO

class ArtworkEmotionSimilarityDAO(SimilarityDAO):
    
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
        self.interactionIDColumn = 

    def elemLayer(self,elem):
        return len(elem)
    
    def getIconClassList(self, elem):
        iconClassList = self.data.loc[elem][self.similarityColumn].split("; ")
        iconClassList = [iconClass.split(" ")[0] for iconClass in iconClassList if iconClass]
        return iconClassList  
    
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
        """       
        print("elemA: " + elemA)
        print("elemB: " + elemB)
        print("commonAncestor: " + commonAncestor)
        print("distance: " + str(1 - sim))
        print("\n")
        """
        
        # Get first common characters 
        # https://stackoverflow.com/questions/18715688/find-common-substring-between-two-strings
        commonAncestor = os.path.commonprefix([elemA, elemB])
        maxLayer = max(self.elemLayer(elemA), self.elemLayer(elemB))
        if (maxLayer <= 0):
            sim = 0
        else:
            sim = self.elemLayer(commonAncestor) / maxLayer
            
        return 1 - sim

    def iconClassDistance(self, elemA, iconClassListB):
        """
        Computes the distance between an iconClass elem from artwork A and the iconClass elements from artwork B
        
        a) It finds the iconClass elem in iconClassListB with the largest common prefix with elemA and compares it.
        b) If none are found, distance is set to 1.
        
        Parameters
        ----------
        elemA: String
            Iconclass id belonging to artwork A
        iconClassListB: list
            List of iconclass id belonging to artwork B
        
        Returns
        -------
            distance: float
        """
        longestPrefix = ""
        longestPrefixElemB = ""
        for elemB in iconClassListB:
            prefix = os.path.commonprefix([elemA, elemB])
            if (len(prefix) > len(longestPrefix)):
                longestPrefix = prefix
                longestPrefixElemB = elemB
        
        return self.taxonomyDistance(elemA,longestPrefixElemB)
        
        

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
        iconClassListA = self.getIconClassList(elemA)
        iconClassListB = self.getIconClassList(elemB)
        
        # Set largest list to be A and the other B
        if (len(iconClassListB) > len(iconClassListA)):
            aux = iconClassListA
            iconClassListA = iconClassListB
            iconClassListB = aux
        
        print("elemA: " + str(elemA))
        print("elemB: " + str(elemB))
        print("Iconclass A: " + str(iconClassListA))
        print("Iconclass B: " + str(iconClassListB))
        print("\n")
        
        # Compare each element of valueA with the element from B with the biggest common prefix
        # If none from B share a common prefix, distance is equal to 0
        distanceTotal = 0
        for elemA in iconClassListA:
            distance = self.iconClassDistance(elemA,iconClassListB)
            distanceTotal += distance
        
        distanceTotal /= len(iconClassListA)
        print("distanceTotal: " + str(distanceTotal))
        
        return distanceTotal

    
    
    
    
    
    
    
    
    