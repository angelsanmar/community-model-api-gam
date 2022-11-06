# Authors: Guillermo Jimenez-Díaz
#          Jose Luis Jorro-Aragoneses
#          José Ángel Sánchez Martín

import numpy as np

from community_module.similarity.similarity import Similarity
"""
serenity (higher joy)
loive (trust, joy)
interest (higher anticipation)
disapproval (sadness, surprise)
"""

# Arent them in the wrong order???
#PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

PLUTCHIK_EMOTIONS = ['anger', 'anticipation', 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust']
#'disgust', 'fear', 'sadness', 'surprise', 'trust'] # Falta incluir 'joy'

class EmotionSimilarity(Similarity):

    def __init__(self, data):
        """Construct of EmotionSimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of emotions and
            values contain number of times that an emotions is in an element.
        """
        super().__init__(data)
        # Nos quedamos únicamente con las emociones de Plutchik
        self.data = data[PLUTCHIK_EMOTIONS]

    def _dominantEmotion(self, emotions, size=1):
        """Method to obtain dominant emotions of a user.

        Parameters
        ----------
        emotions : pd.Series
            Series that contains the emotions and times of this emotion in dataset.
        size : int, optional
            Number of dominant emotions to recover, by default 1
        """

        return emotions.sort_values(ascending=False).index[:size].values

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
        except ValueError:
            return 1.0
            
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

        emotionsA = self._dominantEmotion(self.data.loc[elemA], numEmotions)
        emotionsB = self._dominantEmotion(self.data.loc[elemB], numEmotions)

        distance = 0
        for i in range(numEmotions):
            distance += self._emotions_distance(emotionsA[i], emotionsB[i])

        return distance / numEmotions

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
