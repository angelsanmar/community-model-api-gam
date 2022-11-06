# Authors: Guillermo Jimenez-Díaz
#          Jose Luis Jorro-Aragoneses
#          José Ángel Sánchez Martín

import numpy as np
import pandas as pd
import math

from community_module.similarity.emotionSimilarity import EmotionSimilarity


# Arent them in the wrong order???
#PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

PLUTCHIK_EMOTIONS = ['Anger', 'Anticipation', 'Joy', 'Trust', 'Fear', 'Surprise', 'Sadness', 'Disgust']
#'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

class GamSophiaEmotionSimilarity(EmotionSimilarity):

    def __init__(self, data):
        """Construct of EmotionSimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of emotions and
            values contain number of times that an emotions is in an element.
        """
        self.data = data
        #print(self.data)
        
    def floor(self,x,digits = 2):
        return math.floor(x*100)/100

    def _dominantEmotion(self, emotions, artwork,user,size=1):
        """
        Method to sort the dominant emotions of a user.

        Parameters
        ----------
        emotions : dict
            Dict with emotions (keys) and confidence level (values)
        size : int (optional)
            Number of dominant emotions to recover, by default 1
        """
        
        """
        print("dominant emotion")
        print(user)
        print(emotions)
        print("\n")
        """
        print("dominant emotion function")
        print(user)
        print(emotions)
        print(artwork)
        
        
        # Change array into dictionary
        emotionsDict = {}
        for emotion in emotions:
            emotionsDict = emotionsDict | emotion
        print(emotionsDict)
        print("\n")
        
        listEmotions = sorted(emotionsDict.items(), key=lambda x:x[1], reverse=True)#[0:size] 
        sortEmotions =dict(listEmotions)
        
        """
        print(listEmotions)
        print(sortEmotions)
        print("dominantEmotion2")
        print("\n")
        """

        return sortEmotions
        
    def distanceEmotionsDict(self, emotionDictA, emotionDictB):
        """
        Method to calculate the distance between 2 emotions (dict) based on PLUTCHKIN emotions.
        It computes the emotion distance between each key of dict (emotionA) and each key of dict (emotionB) according to the confidence level
            

        Parameters
        ----------
        emotionA : dict of Plutchick emotions (key: emotion, value: confidence level)
            First emotion.
        emotionB : dict of Plutchick emotions (key: emotion, value: confidence level)
            Second emotion.

        Returns
        -------
        double
            Distance value between emotions.
        """
        emotionListA = list(emotionDictA.keys())
        emotionListB = list(emotionDictB.keys())
        emotionSize = min(3,len(emotionListA),len(emotionListB))
        
        distanceTotal = 0
        for i in range(emotionSize):
            emotionA = emotionListA[i]
            emotionB = emotionListB[i]
            distance = self._emotions_distance(emotionA, emotionB)
            distanceTotal += distance
        
        distanceTotal /= emotionSize
        return distanceTotal
    
    
    """
    Fix it later. It has problems like comparing one with itself
    e.g: joy, sadness  vs joy, sadness
    joy will be 0 distance, but sadness will be 1 (so it will be 0.5)
    """
    
    def distanceEmotionsDictOLD(self, emotionDictA, emotionDictB):
        """
        Method to calculate the distance between 2 emotions (dict) based on PLUTCHKIN emotions.
        It computes the emotion distance between each key of dict (emotionA) and each key of dict (emotionB) according to the confidence level
            

        Parameters
        ----------
        emotionA : dict of Plutchick emotions (key: emotion, value: confidence level)
            First emotion.
        emotionB : dict of Plutchick emotions (key: emotion, value: confidence level)
            Second emotion.

        Returns
        -------
        double
            Distance value between emotions.
        """
        print("distanceEmotionsDict")
        print(emotionDictA)
        print(emotionDictB)
        
        distanceTotal = 0
        confidenceTotal = 0
        for emotionA, confidenceA in emotionDictA.items():
            for emotionB, confidenceB in emotionDictB.items():
                distance = self._emotions_distance(emotionA, emotionB)
                distance = self.floor(distance,2)
                print("distance " + str(emotionA) + "; " + str(emotionB) + " = " + str(distance))
                # Apply correction based on confidence level.
                confidenceMean = (confidenceA + confidenceB) / 2
                confidenceMean = 1
                distance = distance * confidenceMean
                distance = self.floor(distance,2)
                print("distance confidence " + str(confidenceMean) + " = " + str(distance))
                
                
                distanceTotal += distance
                confidenceTotal += confidenceMean
                
        distanceTotal =  self.floor(distanceTotal / confidenceTotal,2)
        
        print("\n")
        print("distanceTotal: " + str(distanceTotal))
        print("confidence total: " + str(confidenceTotal))
        print("\n")
        return distanceTotal
        
    def _emotions_distance(self, emotionA, emotionB):
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
            return 0

    def distance(self, elemA, elemB, numEmotions = 3):
        """Method to obtain the distance between two element based on the array of emotions.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.
        numEmotions : int, optional
            Number of most represented emotions to calculate the distance, by default 3

        Returns
        -------
        double
            Distance between the two elements.
        """
        # Get artworks visited by user1 (elemA) and visited by user2 (elemB)
        artworksA = self.data.loc[elemA]
        artworksB = self.data.loc[elemB]

        commonArtworks = self.data.loc[[elemA,elemB]].dropna(axis=1)
        commonArtworks = commonArtworks[~commonArtworks.index.duplicated(keep='first')]
        
        # For each of the artworks calculate the distance in emotion, then apply the mean
        # https://stackoverflow.com/questions/45990001/forcing-pandas-iloc-to-return-a-single-row-dataframe
        emotionsA = commonArtworks.loc[elemA]#.iloc[0]
        emotionsB = commonArtworks.loc[elemB]#.iloc[0]

        userDistance = 0
        numEmotions = 1
        for i in range(len(commonArtworks.columns)):
            emotionDictA = self._dominantEmotion(emotionsA.iloc[i],commonArtworks.columns[i],elemA,numEmotions)
            emotionDictB = self._dominantEmotion(emotionsB.iloc[i],commonArtworks.columns[i],elemB,numEmotions)
            userDistance2 = 0
            
            userDistance2 += self.distanceEmotionsDict(emotionDictA, emotionDictB)
            userDistance = userDistance + userDistance2

        return userDistance / max(len(commonArtworks.columns),1)

    def similarity(self, elemA, elemB, numEmotions = 3):
        """Method to obtain the similarity between two element based on the array of emotions.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.
        numEmotions : int, optional
            Number of most represented emotions to calculate the similarity, by default 3

        Returns
        -------
        double
            Similarity between the two elements.
        """
        return 1 - self.distance(elemA, elemB, numEmotions) # ¿No debería ser 1 / distancia?
