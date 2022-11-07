# Authors: José Ángel Sánchez Martín
import os
import json

import numpy as np

from community_module.similarity.similarityDAO import SimilarityDAO
from community_module.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from dao.dao_json import DAO_json


class InteractionSimilarityDAO(SimilarityDAO):
    """
    Class to compute the interaction similarity between two users
    
    a) It computes the distanceMatrix between the objects the users interacted with (interaction objects (IO))
    b) For each IO userA interacted with, it gets the IO userB interacted with most similar to it.
    c) It computes the similarity between interaction attributes on these two IOs (e.g., emotions associated to IO(A) vs emotions associated to IO(B))
    """
    
    def __init__(self, dao, perspective):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao)
        self.perspective = perspective
        
        
        # Interaction similarity function
        self.similarityFunction = self.perspective["interaction_similarity_functions"][0]
        self.similarityColumn = self.similarityFunction['sim_function']['on_attribute']['att_name']
        
        self.interactionSimilarityMeasure = self.initializeFromPerspective(dao, self.similarityFunction)
        #print(self.interactionSimilarityMeasure)
        
        
        
        # Remove the interactions with emotion with interactionSimilarityMeasure empty
        IOColumn = self.similarityFunction['sim_function']['interaction_object']['att_name']
        df = self.data.copy()
        df2 = df.explode([self.similarityColumn, IOColumn])
        df3 = df2.loc[ df2[self.similarityColumn].str.len() != 0 ]
        
        """
        print("\n")
        df3_check = df3[df3['userName'] == 'RQ4a2nIG']
        print(df3_check[['userName', IOColumn, self.similarityColumn]])
        
        
        df3 = df2.copy()
        """
        
        """
        df3_1 = df3.drop(IOColumn, axis=1)
        df3_2 = df3.copy()

        
        keys = lambda x: (x.userName,x.relationship_with_arts, x.relationship_with_museums, x.IdArtefact)
        """

        df4 = df3.groupby(['userName', 'relationship_with_arts', 'relationship_with_museums']).agg(list)         
        df4 = df4.reset_index() 
        
        """
        idArtefacts = df4.apply(lambda row: row[IOColumn][0], axis = 1)
        df4[IOColumn] = idArtefacts
        """
    
   
        # Add column to save dominant interaction attribute
        df4[self.similarityColumn + 'DominantInteractionGenerated'] = [[] for _ in range(len(df4))]
        
        
        #print(self.data[['userName',self.similarityColumn, 'relationship_with_arts']])
        
        self.data = df4.copy()
        
        """
        print(self.data[['userName', IOColumn, self.similarityColumn]])
        print(len(self.data[IOColumn][3]))
        print(len(self.data[self.similarityColumn][3]))
        """
        
        
        """
        print("df4")
        print(df4[['userName',self.similarityColumn, 'relationship_with_arts']])
        """
        
        
        """
        print("df2 exploded")

        print(df2[['userName',self.similarityColumn]])
        
        print("\n\n\n")
        
        print("df3")
        print(df3[['userName',self.similarityColumn]])
        
        print("\n\n\n")
        
        print("df4")
        print(df4[['userName',self.similarityColumn]])
        """
        
        # Get IO distance matrix
        file = self.interactionObjectDistanceMatrixRoute()
        if (os.path.exists(file)):
            self.distanceDict = self.getIODistanceMatrixFromFile(file)
        else:
            self.distanceDict = self.computeIODistanceMatrix()
                
        #self.IO_distanceIndex = list(map(int, self.distanceDict['index']))
        self.IO_distanceIndex = self.distanceDict['index']
        self.IO_distanceMatrix = np.asarray(self.distanceDict['distanceMatrix'])
        
        """
        print("artwork distance matrix")
        print(self.IO_distanceIndex)
        print(self.IO_distanceMatrix)
        
        """
        
        
        
    
    def interactionObjectDistanceMatrixRoute(self):
        abspath = os.path.dirname(__file__)
        relpath = "../../communityModel/" + "interactionObjects/" + self.perspective['name'] + ".json"
        exportFile = os.path.normpath(os.path.join(abspath, relpath))
        
        return exportFile
    
    def getInteractionObjectDAO(self):
        #route = 'data/GAM_Catalogue_plus.json'
        
        abspath = os.path.dirname(__file__)
        relpath = "../../communityModel/data/GAM_Catalogue_plus.json"
        # route = os.path.normpath(os.path.join(abspath, relpath))
        route = os.path.normpath(os.path.join(abspath, relpath))
        #print("hey")
        
        print("abspath: " + str(abspath))
        print("relpath: " + str(relpath))
        print("route: " + str(route))

        daoJson = DAO_json(route)
        
        return daoJson
    
    def getInteractionObjectData(self):
        daoJson = self.getInteractionObjectDAO()
        return daoJson.getPandasDataframe()
        

    def getIODistanceMatrixFromFile(self, file):
        """
        Method to directly assign already calculated distance matrixes

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """
        with open(file, 'r', encoding='utf8') as f:
            IO_distanceDict = json.load(f)
                
        return IO_distanceDict
        
    def computeIODistanceMatrix(self):
        """
        Method to calculate the distance matrix between all interaction objects included in data.

        Returns
        -------
        IO_distanceDict: dict
            Includes distance between interaction objects
                index:
                    IO index
                distanceMatrix: np.array
                    Matrix that contains all similarity values.
        """
        # Calculate interaction object (IO) similarity
        similarity_functions = self.perspective['similarity_functions']
        daoJson = self.getInteractionObjectDAO()
        IO_similarityMeasure = ComplexSimilarityDAO(daoJson,similarity_functions)
        IO_distanceMatrix = IO_similarityMeasure.matrix_distance()
        
        # Export _id (id artefact) and distance matrix to json file
        IO_distanceDict = {}
        IO_distanceDict['index'] = IO_similarityMeasure.data['_id'].tolist()
        IO_distanceDict['distanceMatrix'] = IO_distanceMatrix.tolist()
        
        exportFile = self.interactionObjectDistanceMatrixRoute()
        
        with open(exportFile, "w") as outfile:
            json.dump(IO_distanceDict, outfile, indent=4)
        
        return IO_distanceDict
        
    def getSimilarIOIndex(self, objectA, IOB):
        """
        Method to obtain the index of the object in IOB that is most similar to objectA
        
        Distance between IOs in the database are calculated beforehand (distanceMatrix). 
        Only IOs above a given x (0.7) are considered similar. If IOB doesn't include a similar object to objectA, the function returns -1.

        Parameters
        ----------
        objectA : object (int, String...)
            IDs of an object userA interacted with
        elemB : list
            List of IDs belonging to the objects userB interacted with.

        Returns
        -------
        double
            Index in the list IOB of the object userB interacted with that is most similar to objectB 
            -1 if all objects in IOB are not similar to objectA
        """
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-31.php
        # https://stackoverflow.com/questions/15287084/numpy-find-the-values-of-rows-given-an-array-of-indexes
        # https://stackoverflow.com/questions/33678543/finding-indices-of-matches-of-one-array-in-another-array
        
        
        # Sometimes objectA is not in the artworks catalogue (ask about this)
        try:
            # Convert to string the object ids because in some cases artwork data has string ids while interactions have int ids
            objectA = str(objectA)
            IOB = list(map(str, IOB))
            
            """
            print("type object A: " + str(type(objectA)))
            print("type IO_distanceIndex: " + str(type(self.IO_distanceIndex[0])))
            print("objectA: " + str(objectA))
            print("IOB: " + str(IOB))
            print("\n")
            """
        
            objectAIndex = self.IO_distanceIndex.index(str(objectA))
            distanceMatrix_IOB_indexes = np.nonzero(np.in1d(self.IO_distanceIndex,IOB))[0]
            distanceMatrix_IOB_values = self.IO_distanceMatrix[objectAIndex, distanceMatrix_IOB_indexes]
            mostSimilarIOIndex = distanceMatrix_IOB_values.argmin()
            mostSimilarIO = IOB[mostSimilarIOIndex]  
            
            """
            print("type object A: " + str(type(objectA)))
            print("type IO_distanceIndex: " + str(type(self.IO_distanceIndex[0])))
            print("objectA: " + str(objectA))
            print("IOB: " + str(IOB))
            print("\n")
            print("IO_distanceIndex: " + str(self.IO_distanceIndex))
            print(self.IO_distanceMatrix)
            print("\n")
            print("objectA index: " + str(objectAIndex))
            print("distanceMatrix_IOB_indexes: " + str(distanceMatrix_IOB_indexes))
            print("distanceMatrix_IOB_values: " + str(distanceMatrix_IOB_values))
            print("minimumDistance index: " + str(mostSimilarIOIndex))
            print("minimumDistance value: " + str(distanceMatrix_IOB_values[mostSimilarIOIndex]))
            print("most similar IO: " + str(mostSimilarIO))
            print("\n\n\n")
            
            """
            
            # Get index of elements above a given threshold (let is say 0.5)
            
            
            # If the best match is still dissimilar
            """
            if (distanceMatrix_IOB_values[mostSimilarIOIndex] >= 0.4):
                mostSimilarIOIndex = -1
            """
            
            return mostSimilarIOIndex
        
        except ValueError:
            
            print("exception ")
            print("type object A: " + str(type(objectA)))
            """
            """
            print("objectA: " + str(objectA))
            print("IO_distanceIndex: " + str(self.IO_distanceIndex))
            
            objectAIndex = self.IO_distanceIndex.index(str(objectA))
            print("objectA index: " + str(objectAIndex))
            distanceMatrix_IOB_indexes = np.nonzero(np.in1d(self.IO_distanceIndex,IOB))[0]
            print("distanceMatrix_IOB_indexes: " + str(distanceMatrix_IOB_indexes))
            distanceMatrix_IOB_values = self.IO_distanceMatrix[objectAIndex, distanceMatrix_IOB_indexes]
            print("distanceMatrix_IOB_values: " + str(distanceMatrix_IOB_values))
            mostSimilarIOIndex = distanceMatrix_IOB_values.argmin()
            print("most similar IO Index: " + str(mostSimilarIOIndex))
            mostSimilarIO = IOB[mostSimilarIOIndex]
            print("most similar IO: " + str(mostSimilarIO))
            
            print("end exception")
            
            return -1
            
        
        """
       """

    def distance(self,elemA, elemB):
        """
        Method to obtain the distance between two element.

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
        userInteractionA = self.data.loc[elemA]
        userInteractionB = self.data.loc[elemB]
        
        """
        print(userInteractionA['userName'])
        print(userInteractionB['userName'])
        """

        # Get interaction objects (IO) the user interacted with
        # print(self.similarityFunction)
        IOColumn = self.similarityFunction['sim_function']['interaction_object']['att_name']
        IOA = userInteractionA[IOColumn]
        IOB = userInteractionB[IOColumn]
        
        """
        print("IO Columns")
        print(IOColumn)
        print(IOA)
        print(IOB)
        print("\n\n\n")
        """
        
        # Set largest list to be A and the other B
        exchanged = False
        if (len(IOB) > len(IOA)):
            exchanged = True
            IOA, IOB = self.exchangeElements(IOA,IOB)
            userInteractionA, userInteractionB = self.exchangeElements(userInteractionA, userInteractionB)
        
        # Initialize distance
        distanceTotal = 0
        # Dominant interaction attribute value
        dominantInteractionAttribute = ""
        
        try:
        
            # For each IO in A, get most similar IO in B
            for objectIndexA in range(len(IOA)):
                objectA = IOA[objectIndexA]
                objectIndexB = self.getSimilarIOIndex(objectA, IOB)
                
                #print("objectA: " + str(objectA))
                
                
                if (objectIndexB != -1):
                    """
                    print("interactionsA: " + str(userInteractionA[self.similarityColumn]))
                    print("interactionsB: " + str(userInteractionB[self.similarityColumn]))
                    print("objectIndexA: " + str(objectIndexA))
                    print("len IOA: " + str(len(IOA)))
                    print("IOA: " + str(IOA))
                    print(userInteractionA['userName'])
                    
                    """
                    
                    
                    # Get interaction similarity feature associated to IO A and IO B
                    interactionFeatureA = userInteractionA[self.similarityColumn][objectIndexA]
                    interactionFeatureB = userInteractionB[self.similarityColumn][objectIndexB]
                    
                    """
                    print("interactionFeatureA: " + str(interactionFeatureA))
                    print("interactionFeatureB: " + str(interactionFeatureB))
                    
                    
                    """
                    
                    # Calculate distance between them
                    distance = self.interactionSimilarityMeasure.distanceValues(interactionFeatureA, interactionFeatureB)

                    # Add dominant interaction value to list (e.g., emotions = {joy: 3, sadness: 4, trust: 1} -> sadness
                    dominantInteractionAttributeA, dominantInteractionAttributeB = self.interactionSimilarityMeasure.dominantValue(interactionFeatureA, interactionFeatureB)
                    """
                    print("dominantA: " + str(dominantInteractionAttributeA))
                    print("dominantB: " + str(dominantInteractionAttributeB))
                    
                    """

                    if (exchanged):
                        dominantInteractionAttribute = dominantInteractionAttributeB
                    else:
                        dominantInteractionAttribute = dominantInteractionAttributeA
                    
                else:
                    distance = 1
                
                """
                print("distance: " + str(distance))
                print("distanceTotal: " + str(distanceTotal))
                print("\n\n")
                
                """
                
                """
                """
                distanceTotal += distance
                
            """ 
            distanceTotal /= len(IOA)
            print("distanceTotal (FINAL): " + str(distanceTotal))
            print("\n\n")
         
            """
            
        except Exception as e:
            print("\n\n\n")
            print("Exception dominant attribute")
            print(str(e))
            print("elemA: " + str(elemA))
            print("elemB: " + str(elemB))
            print("IOA: " + str(IOA))
            print("IOB: " + str(IOB))
            print("interactionsA: " + str(userInteractionA[self.similarityColumn]))
            print("interactionsB: " + str(userInteractionB[self.similarityColumn]))
            print("objectIndexA: " + str(objectIndexA))
            print("len IOA: " + str(len(IOA)))
            print("IOA: " + str(IOA))
            print(userInteractionA['userName'])
            
            # Get interaction similarity feature associated to IO A and IO B
            interactionFeatureA = userInteractionA[self.similarityColumn][objectIndexA]
            interactionFeatureB = userInteractionB[self.similarityColumn][objectIndexB]

            print("interactionFeatureA: " + str(interactionFeatureA))
            print("interactionFeatureB: " + str(interactionFeatureB))
                    
            print("\n\n\n")
            
            
        
        # Set dominant interaction attribute list
        dominantInteractionAttributeList = self.data.loc[elemA][self.similarityColumn + 'DominantInteractionGenerated']
        
        #print(self.data[[self.similarityColumn]])
        
        """
        print("dominantInteractionAttributeList: " + str(dominantInteractionAttributeList))
        print("distanceTotal: " + str(distanceTotal))
        print("\n\n")
        
        """
            
        dominantInteractionAttributeList.append(dominantInteractionAttribute)
        self.data.at[elemA, self.similarityColumn + 'DominantInteractionGenerated'] = dominantInteractionAttributeList
        
        return distanceTotal
        
        
        
        
        
    
    
    