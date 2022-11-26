from bson.json_util import dumps, loads


from context import dao
from dao.dao_db import DAO_db

from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient

import json
import pandas as pd
import os

from communityModel.inSpiceDataFormatter import InSpiceDataFormatter


class DAO_db_interactionDatas(DAO_db):
    """
    DAO for accessing flag related data in MongoDB
    """

    # def __init__(self, db_host="mongodb", db_port=27017, db_user="spice", db_password="spicepassword", db_name="spiceComMod"):
    def __init__(self):
    # def __init__(self, db_host="mongodb", db_port=27017, db_user="spice", db_password="spicepassword", db_name="spiceComMod"):
    
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

    def getInteractionDataById(self, id):
        """
        :Return:
            List with all flags, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_interactionData.find({"_id": id})
        dataList = loads(dumps(list(dataList)))
        print(dataList[0])
        return dataList[0]

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
        
        user_interactions = InSpiceDataFormatter().formatData(annotated_stories_df)

        return user_interactions
        
    def exportFilename(self, filename):
        abspath = os.path.dirname(__file__)
        relpath = filename
        route = os.path.normpath(os.path.join(abspath, relpath))
        
        return route
        
    