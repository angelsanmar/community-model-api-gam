# Authors: José Ángel Sánchez Martín
import os
from community_module.similarity.similarityDAO import SimilarityDAO

PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust']
PLUTCHIK_EMOTIONS_2 = ['Anger', 'Anticipation', 'Joy', 'Trust', 'Fear', 'Surprise', 'Sadness', 'Disgust']

class PlutchikEmotionSimilarityDAO(SimilarityDAO):
    
    def __init__(self, dao, similarityFunction):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao, similarityFunction)

    
    def distanceEmotions(self, emotionA, emotionB):
        """Method to calculate the distance between 2 emotions based on PLUTCHKIN emotions.

        Parameters
        ----------
        emotionA : str
            First emotion.
        emotionB : str
            Second emotion.

        Returns
        -------
        double
            Distance value between emotions.
        """
        try: 
            indexA = PLUTCHIK_EMOTIONS.index(emotionA)
            indexB = PLUTCHIK_EMOTIONS.index(emotionB)

            if indexB > indexA:
                indexA, indexB = indexB, indexA

            return min( (indexA - indexB) / 4, (indexB - indexA + 8) / 4)
        # We don't have a Plutchick emotion for that user and artwork
        except ValueError:
            return 1.0
    
    def distanceValues(self, emotionsDictA, emotionsDictB):
        """
        Method to obtain the distance between two combination of emotions
        
        a) Get common emotions.
        b) For the different emotions (diffA, diffB), compute distance between each element in diffA and the most similar emotion in diffB

        Parameters
        ----------
        emotionsDictA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        emotionsDictB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        double
            Distance between the two combination of emotions.
        """
        """
        print("distanceValues plutchik: ")
        print(type(emotionsDictA))
        print(type(emotionsDictB))
        print(emotionsDictA)
        print(emotionsDictB)
        print("\n\n\n")
        """
        
        emotionsDictA = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictA.items() if x.startswith('emotion:')])
        emotionsDictB = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictB.items() if x.startswith('emotion:')])
        
        
        if (len(emotionsDictA) <= 0 or len(emotionsDictB) <= 0):
            return 1.0
        else:
            # Get emotions with highest confidence value (dominant emotion)
            emotionA = max(emotionsDictA, key=emotionsDictA.get).lower()
            emotionB = max(emotionsDictB, key=emotionsDictB.get).lower()
            
            """
            print("emotionsA: " + str(emotionsDictA))
            print("emotionsB: " + str(emotionsDictB))
            print("emotionA: " + str(emotionA))
            print("emotionB: " + str(emotionB))
            """
            
            return self.distanceEmotions(emotionA,emotionB)
        
        
        
        
        """
        emotionsA = set(emotionsDictA.keys())
        emotionsB = set(emotionsDictB.keys())
        
        commonEmotions = emotionsA.intersection(emotionsB)
        
        diffEmotionsA = [i for i in emotionsA if i not in commonEmotions]
        diffEmotionsB = [i for i in emotionsB if i not in commonEmotions]
        
        # Set largest list to be A and the other B
        if (len(diffEmotionsA) > len(diffEmotionsB)):
            aux = diffEmotionsA
            diffEmotionsA = diffEmotionsB
            diffEmotionsB = aux
        
        # Get similarity between two emotions
        
        
        print(self.similarityColumn)
        
        print("emotionsA: " + str(emotionsA))
        print("emotionsB: " + str(emotionsB))
        print("common emotions: " + str(commonEmotions))
        print("diff emotions A: " + str(diffEmotionsA))
        print("diff emotions B: " + str(diffEmotionsB))
        print("\n")
        
        return 1.0
        """
        
    def dominantValue(self, emotionsDictA, emotionsDictB):
        """
        Method to obtain the dominant value in each combination of emotions
        
        Parameters
        ----------
        emotionsDictA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        emotionsDictB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        String
            Dominant emotion for A and B
        """
        emotionsDictA = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictA.items() if x.startswith('emotion:')])
        emotionsDictB = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictB.items() if x.startswith('emotion:')])
        
        
        if (len(emotionsDictA) <= 0):
            emotionA = ""
        else:
            emotionA = max(emotionsDictA, key=emotionsDictA.get).lower()
            
        if (len(emotionsDictB) <= 0):
            emotionB = ""
        else:
            emotionB = max(emotionsDictB, key=emotionsDictB.get).lower()
        
        
        return emotionA, emotionB
    
    
    