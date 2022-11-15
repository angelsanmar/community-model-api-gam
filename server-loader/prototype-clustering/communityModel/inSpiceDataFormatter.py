import pandas as pd
from context import community_module

from communityModel.dataLoader import DataLoader


class InSpiceDataFormatter():


    def userDataRoute(self):
        return DataLoader().fileRoute("data/GAMGame_users_RN_UNITO.json")
    
    def formatData(self, annotated_stories_df):
        """
        Interaction Pandas DataFrame

        Parameters
        ----------


        Returns
        -------
        pd.DataFrame
            Pandas dataframe with the interaction data.
        """
        print("dao_db_interaction data")
        
        """
        dbData = self.getInteractionData()['data']
        data = json.dumps(dbData)
        annotated_stories_df = pd.read_json(data)
        """
        
        # Explode the list of user-artwork interactions
        df = annotated_stories_df.explode('parts')
        df = df.reset_index()
        
        # Get artworkId, emotions, sentiments
        df2_a = pd.json_normalize(df["parts"], max_level = 0)
        
        # Get itMakesMeFeel attribute which is needed for the visualization
        df2_b = pd.json_normalize(df2_a["multimediaData"], max_level = 0)
        df2_b = pd.json_normalize(df2_b["answersToTemplates"], max_level = 0)
        df2_b = df2_b.rename(columns = {'itMakesMeFeel':'ItMakesMeFeel'})

        # Interactions user-artwork dataframe
        df2 = pd.concat([df2_a,df2_b], axis=1, join='inner')
        df2
        
        # Combine user and interaction data
        df3 = pd.concat([df,df2], axis=1, join='inner')
        
#--------------------------------------------------------------------------------------------------------------------------
#    Remove interactions without a valid artwork
#--------------------------------------------------------------------------------------------------------------------------
        
        artworksFilename = DataLoader().fileRoute("data/GAM_Catalogue_plus.json")
        artworks = pd.read_json(artworksFilename)
        artworks['artworkId'] = artworks['_id'].astype(str)
        df4 = pd.merge(df3,artworks, on='artworkId', how='right')
        
        print("df4 after merging with artworks")
        print(df4)
        print("\n\n\n")
        
#--------------------------------------------------------------------------------------------------------------------------
#   Group by user
#--------------------------------------------------------------------------------------------------------------------------
        
        # Set default values
        """
        values = {'emotions':  {}}
        df3 = df3.fillna(value=values)
        """
        df4['emotions'] = df4['emotions'].apply(lambda x: {} if x != x else x)
        
        # Rename to fit the same format as GAM_RN_User_interactions
        df5 = df4.groupby("authorUsername").agg(list)
        df5 = df5.reset_index()
        df6 = df5.rename(columns = {'authorUsername':'userName'})
        
        print("df4 dao_db_interaction data")
        


#--------------------------------------------------------------------------------------------------------------------------
#    # Combine with user data
#--------------------------------------------------------------------------------------------------------------------------
        
        users = pd.read_json(self.userDataRoute())  
        user_interactions = pd.merge(df6, users, on='userName', how='left')
        
        # Set default values
        values = {'relationship_with_arts': 'unknown', 'relationship_with_museums': 'unknown'}
        user_interactions = user_interactions.fillna(value=values)
        
        print("end dao_db_interaction data")
        
        
        print(user_interactions)
        
        
        print("\n\n\n")

        return user_interactions