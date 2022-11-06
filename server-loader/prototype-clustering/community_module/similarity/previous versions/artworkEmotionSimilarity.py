# Authors: Guillermo Jimenez-Díaz
#          Jose Luis Jorro-Aragoneses
#          José Ángel Sánchez Martín

import numpy as np
import pandas as pd

from community_module.similarity.emotionSimilarity import EmotionSimilarity


# Arent them in the wrong order???
#PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust']
#'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

class ArtworkEmotionSimilarity(EmotionSimilarity):

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
        
    

    def _dominantEmotion(self, emotions, emotionsAbs,user,size=1):
        """Method to obtain dominant emotions of a user.

        Parameters
        ----------
        emotions : pd.Series
            Series that contains the emotions and times of this emotion in dataset.
        size : int, optional
            Number of dominant emotions to recover, by default 1
        """
        
        #return emotions.sort()[:size]
        try:
            emotionsList = emotions.split(", ")
            return emotionsList[:size]
        except:
            print(user)
            print(emotionsAbs)
            print(emotions)
        
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
        
        #print(artworksA)
        #print(artworksB)
        
        # https://www.geeksforgeeks.org/how-to-drop-columns-with-nan-values-in-pandas-dataframe/
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
        # Remove the artworks without emotions from both users (axis: 0 (x; rows) 1 (y; columns)
        commonArtworks = self.data.loc[[elemA,elemB]].dropna(axis=1)
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
        # https://stackoverflow.com/questions/13035764/remove-pandas-rows-with-duplicate-indices
        commonArtworks = commonArtworks[~commonArtworks.index.duplicated(keep='first')]
        """
        print(self.data)
        print(commonArtworks)
        print(type(self.data))
        print(type(commonArtworks))
        result = commonArtworks.duplicated()
        print(result)
        print("\n\n")
        print("\n\n\n")
        
        print(elemA)
        print(elemB)
        print("\n\n\n")
        print(commonArtworks)
        print("\n\n\n")
        
        print("\n\n\n")
                

        """
        
        
        # For each of the artworks calculate the distance in emotion, then apply the mean
        # https://stackoverflow.com/questions/45990001/forcing-pandas-iloc-to-return-a-single-row-dataframe
        emotionsA = commonArtworks.loc[elemA]#.iloc[0]
        emotionsB = commonArtworks.loc[elemB]#.iloc[0]
        """
        print("werwer")
        print(type(emotionsA))
        print(emotionsA)
        emoA = emotionsA.iloc[3]
        print(emoA)
        print("check")
        
        print("\n\n")
        print(emotionsA)
        print("\n\n")
        print(emotionsB)
        print("\n\n")
"""
        
        
        userDistance = 0
        numEmotions = 1
        # https://www.statology.org/pandas-iterate-over-dataframe-columns/
        for i in range(len(commonArtworks.columns)):
            dominantEmotionA = self._dominantEmotion(emotionsA.iloc[i],emotionsA,elemA,numEmotions)
            dominantEmotionB = self._dominantEmotion(emotionsB.iloc[i],emotionsB,elemB,numEmotions)
            userDistance2 = 0
            for j in range(numEmotions):
                userDistance2 += self._emotions_distance(dominantEmotionA[j],dominantEmotionB[j])
            userDistance2 = userDistance2 / numEmotions
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
