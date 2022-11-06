# Authors: José Ángel Sánchez Martín, Jose Luis Jorro-Aragoneses
import numpy as np
import statistics

class ExplainedCommunitiesDetection:
    """Class to search all communities that all members have a common
    propertie. This algorithm works with clustering techniques.
    """

    def __init__(self, algorithm, data, distanceMatrix, perspective = {}):
        """Method to configure the detection algorithm.

        Args:
            data (DataFrame): Data used to apply the similarity measure between
            users.
            algorithm (Class): Class of clustering technique.
            sim (str/Class, optional): Similarity function used in clustering
            technique. Defaults to 'euclidean'.
        """
        self.algorithm = algorithm
        self.data = data
        self.distanceMatrix = distanceMatrix
        self.perspective = perspective
        
        if (len(self.perspective) == 0):
            self.explanaible_attributes = self.data.columns
            self.user_attributes = []
        else:
        
            self.explanaible_attributes = []
            #for similarityFunction in self.perspective['similarity_functions']:
            for similarityFunction in self.perspective['interaction_similarity_functions']:
                self.explanaible_attributes.append(similarityFunction['sim_function']['on_attribute']['att_name'])   
            
            self.user_attributes = []
            for userAttribute in self.perspective['user_attributes']:
                self.user_attributes.append(userAttribute['att_name'])
        

    def search_all_communities(self, answer_binary=False, percentage=1.0):
        """Method to search all explainable communities.

        Args:
            answer_binary (bool, optional): True to indicate that a common property
            occurs only when all answers are 1.0. Defaults to False.
            percentage (float, optional): Value to determine the minimum percetage of
            commons answers to detect a community. Defaults to 1.0.

        Returns:
            int: Number of communities detected.
            dict: Dictionary where each user is assigned to a community.
        """
        n_communities = 2
        finish_search = False
        

        while not finish_search:
            community_detection = self.algorithm(self.data)
            result = community_detection.calculate_communities(distanceMatrix = self.distanceMatrix, n_clusters=n_communities)
            
            # Asignamos a cada elemento su cluster/comunidad correspondiente (fix this later)
            ids_communities = {}
            for i in range(len(self.data.index)):
                ids_communities[self.data.index[i]] = result[i]
                
            result2 = result
            result = ids_communities
            
            complete_data = self.data.copy()
            complete_data['community'] = result.values()

            # Comprobamos que para cada grupo existe al menos una respuesta en común
            explainables = []
            self.communities = complete_data.groupby(by='community')
            
            #for c in range(n_communities):
            n_clusters = min(n_communities,len(set(result2)))
            for c in range(n_clusters):
                community = self.communities.get_group(c)
                community = self.simplifyInteractionAttributes(community)
                explainables.append(self.is_explainable(community, answer_binary, percentage))

            finish_search = sum(explainables) == n_communities

            if not finish_search:
                n_communities += 1
        
        # Get medoids
        medoids_communities = self.getMedoidsCommunities(result2)
        
        communityDict = {}
        communityDict['number'] = n_communities
        communityDict['users'] = result
        communityDict['medoids'] = medoids_communities
        communityDict['percentage'] = percentage
        communityDict['userAttributes'] = self.user_attributes
        
        return communityDict
    
    def simplifyInteractionAttributes(self, community):
        """
        Method to obtain the dominant value in the list of interaction attribute values with the other community members.
        
        Parameters
        ----------
        community : pd.dataframe
            Community member information

        Returns
        -------
        community: pd.dataframe
            Updated dataframe including the dominant value for each user-interaction attribute pair in new columns.
            Column name = community_ + 'interaction attribute label'
        """
        for col in self.explanaible_attributes:
            col2 = col + 'DominantInteractionGenerated'
            
            # Get row index of community members
            communityMemberIndexes = np.nonzero(np.in1d(self.data.index,community.index))[0]
            
            # From the attribute list, consider only the ones between the members of the community
            # https://stackoverflow.com/questions/23763591/python-selecting-elements-in-a-list-by-indices
            # Transform attribute list to fit community members
            #community['community_' + col] = community.apply(lambda row: statistics.mode([row[col2][i] for i in communityMemberIndexes]), axis = 1)
            #community['community_' + col] = community_dominantAttributeList
            print("aaaaaaaaaaaaaaaa")
            
        return community
        
        
    def is_explainable(self, community, answer_binary=False, percentage=1.0):
        explainable_community = False
        
        #for col in community.columns.values:
        for col2 in self.explanaible_attributes:
            if col2 != 'community':
                col = "community_" + col2
                
                # https://www.alphacodingskills.com/python/notes/python-operator-bitwise-or-assignment.php
                # (x |= y) is equivalent to (x = x | y)
                if answer_binary:
                    explainable_community |= (len(community[col]) * percentage)  <= community[col].sum()
                else:
                    print("is_explainable")
                    print("col: " + str(col))
                    print("aaaa")
                    print("community: " + str(community))
                    print("bbgb")

                    print("community[col]" + str(community[col]))
                    print("sdffd")
                    print("value_counts: " + str(community[col].value_counts()))
                    print("dsnskdlfj")
                    explainable_community |= (len(community[col]) * percentage) <= community[col].value_counts().max()
        
        return explainable_community
    
    
    
    
    def getMedoidsCommunities(self, clusteringResult):
        """
        Calculates the community medoid (Representative member)
            
        Parameters
        ----------
            clusteringResult [array]
                Array with the communities each data.row belongs to

        Returns
        -------
            communitiesMedoids [<class 'dict'>]
                Dictionary with keys (community id) and values (pandas dataframe with the medoid row)
        """
        
        # Get cluster representative (medoid)
        # The one with the smallest distance to each other datapoint in the cluster
        communities_members = {}
        for i in range(len(clusteringResult)):
            communities_members.setdefault(clusteringResult[i],[]).append(i)
        
        medoids_communities = {}
        for key in communities_members.keys():
            clusterIxgrid = np.ix_(communities_members[key],communities_members[key])
            clusterDistanceMatrix = self.distanceMatrix[clusterIxgrid]
            clusterRepresentativeIndex = np.argmin(np.sum(clusterDistanceMatrix, axis=1))
            clusterRepresentative = communities_members[key][clusterRepresentativeIndex]
            
            medoids_communities[key] = self.data.index[clusterRepresentative]

        return medoids_communities
    
    # Get the percentage of most frequent value for each feature.
    def secondExplanation(self,community):
        modePropertiesCommunity = {}

        for attribute in self.explanaible_attributes:
            counts = community[attribute].value_counts(normalize=True).mul(100)
            modeAttribute = community[attribute].value_counts().idxmax()
            modePropertiesCommunity[attribute] = {}
            modePropertiesCommunity[attribute]['representative'] = modeAttribute
            modePropertiesCommunity[attribute]['percentage'] = counts[modeAttribute]
    
        return modePropertiesCommunity
    
    
    
    def get_community(self, id_community, answer_binary=False, percentage=1.0):
        """Method to obtain all information about a community.

        Args:
            id_community (int): Id or name of community returned by detection method.
            answer_binary (bool, optional): True to indicate that a common property
            occurs only when all answers are 1.0. Defaults to False. Defaults to False.

        Returns:
            dict: All data that describes the community:
                - name: name of community.
                - members: list of index included in this community.
                - properties: common properties of community. It is a dictionary where:
                    each property is identified by column_name of data, and the value is
                    the common value in this column.
        """
        community = self.communities.get_group(id_community)
        community_user_attributes = community[self.user_attributes]

        community_data = {'name': id_community}
        community_data['percentage'] = str(percentage * 100) + " %"
        community_data['members'] = list(community_user_attributes.index.values)

        explainedCommunityProperties = dict()       

        #for col in community.columns.values:
        for col2 in self.explanaible_attributes:
            if col2 != 'community':
                col = "community_" + col2
               # print(community)
                #print(len(community[col]))
                #print('-', col, community[col].value_counts().index[0])
                if answer_binary:
                    if (len(community[col]) * percentage) <= community[col].sum():
                        explainedCommunityProperties[col] = community[col].value_counts().index[0]
                        # print('-', col, community[col].value_counts().index[0])
                else:
                    
                    if (len(community[col]) * percentage) <= community[col].value_counts().max():
                        explainedCommunityProperties[col] = community[col].value_counts().index[0]
                        # Add the predominant emotion
                        #print('-', col, community[col].value_counts().index[0])
                        
                        # print('-', col, community[col].value_counts().index[0])
                        
                        
        # Second explanation   
        community_data['explanation'] = []
        community_data['explanation'].append(explainedCommunityProperties)
        #community_data['explanation'].append(self.secondExplanation(community))
            
            
        return community_data
    
    
    
        