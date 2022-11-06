from sklearn.cluster import OPTICS

class OpticsCommunityDetection:

    def __init__(self, data):
        """Construct of opticsCommunityDetection.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of attributes names and
            values contain the attribute values for each element.
        """
        self.data = data

    #def calculate_communities(self, distanceMatrix, min_cluster_size=2, max_eps=66, xi=.05):
    def calculate_communities(self, distanceMatrix='euclidean', n_clusters=2):
        """
        Method to calculate the communities of elements from data.

        Parameters
        ----------
        metric : str or Class, optional
            Metric used to calculate the distance between elements, by default 'euclidean'. It is
            possible to use a class with the same properties of Similarity.
        n_clusters : int, optional
            Number of clusters (communities) to search, by default 2

        Returns
        -------
        list
            List with the clusters each element belongs to (e.g., list[0] === cluster the element 0 belongs to.) 
        """
        clusters = []
        epsParameter = 1.0
        while len(set(clusters)) < n_clusters and epsParameter > 0:
            epsParameter -= 0.1
            print("calculating dbscan algorithm")
            print("number of clusters: " + str(n_clusters))
            print("eps: " + str(epsParameter))
            print(distanceMatrix)
            print("clusters")
            print(clusters)
            print("\n")
            # run optics
            optics_model = OPTICS(metric="precomputed", min_samples=1, min_cluster_size=1, max_eps=eps_parameter,
                              xi=0.05)
            optics_model.fit(distanceMatrix)
            clusters = optics_model.labels_[optics_model.ordering_]
            
            
        return clusters
