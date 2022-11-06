from bson.json_util import dumps, loads


from context import dao
from dao.dao_db import DAO_db

from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient

import json
import pandas as pd
import os


class DAO_db_interactionDatas(DAO_db):
    """
    DAO for accessing flag related data in MongoDB
    """

    # def __init__(self, db_host="mongodb", db_port=27017, db_user="spice", db_password="spicepassword", db_name="spiceComMod"):
    def __init__(self):
        """
        :Parameters:
            db_host: mongodb address, Default value: "localhost"
            db_port: mongodb port, Default value: 27017
            db_user: mongodb user, Default value: ""
            db_password: mongodb pass, Default value: ""
            db_name: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__()
        self.db_interactionData = self.mongo.spiceComMod.interactiondatas

    def getData(self):
        pass

    def getInteractionData(self):
        """
        :Return:
            List with all flags, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_interactionData.find({}, {"_id": 0})
        dataList = loads(dumps(list(dataList)))
        return dataList[0]

    # def getInteractionData(self, id):
    #     """
    #     :Return:
    #         List with all flags, Type: json List[<class 'dict'>]
    #     """
    #     # data = self.db_users.find({}, {"_id": 0})
    #     dataList = self.db_interactionDatas.find({"perspectiveId": id})
    #     dataList = loads(dumps(list(dataList)))
    #     return dataList[0]

    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_interactionData.delete_many({})

    def insertInteractionData(self, json):
        """
        :Parameters:
            flagJSON: flag associated to the perspective and the user.
        """
        temp = copy(json)
        if type(temp) is list:
            self.db_interactionData.insert_many(temp)
        else:
            self.db_interactionData.insert_one(temp)

    def updateInteractionData(self, json):
        key = {
            'perspectiveId': json['perspectiveId'], 'userid': json['userid']}
        self.db_interactionData.update_one(key, {"$set": json}, upsert=True)


    def deleteInteractionData(self, json):
        """
        :Parameters:
            flagJSON: Flag/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        self.db_interactionData.delete_one(json)
        #self.db_interactionDatas.delete_one({'id': flagId})

    def deleteAllInteractionData(self):
        self.db_interactionData.delete_many({})
    
    
    def getPandasDataframe(self):
        """
        Interaction Pandas DataFrame

        Parameters
        ----------


        Returns
        -------
        pd.DataFrame
            Pandas dataframe with the interaction data.
        """
        dbData = self.getInteractionData()['data']
        data = json.dumps(dbData)
        annotated_stories_df = pd.read_json(data)
        
        # Prepare interaction data for clustering
        df = annotated_stories_df.explode('parts')
        df = df.reset_index()
        
        df2 = pd.json_normalize(df["parts"], max_level = 0)
        df3 = pd.concat([df,df2], axis=1, join='inner')
        
        # Set default values
        """
        values = {'emotions':  {}}
        df3 = df3.fillna(value=values)
        """
        df3['emotions'] = df3['emotions'].apply(lambda x: {} if x != x else x)
        
        df4 = df3.groupby("authorUsername").agg(list)
        df4 = df4.reset_index()
        df5 = df4.rename(columns = {'authorUsername':'userName'})
        
        # Combine with user data
        users = pd.read_json(self.userDataRoute())  
        user_interactions = pd.merge(df5, users, on='userName', how='left')
        
        # Set default values
        values = {'relationship_with_arts': '', 'relationship_with_museums': ''}
        user_interactions = user_interactions.fillna(value=values)

        return user_interactions
        
    def userDataRoute(self):
        abspath = os.path.dirname(__file__)
        relpath = "../communityModel/data/GAMGame_users_RN_UNITO.json"
        route = os.path.normpath(os.path.join(abspath, relpath))
        
        return route
        
