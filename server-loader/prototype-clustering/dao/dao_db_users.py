from bson.json_util import dumps, loads

from context import dao
from dao.dao_class import DAO

from copy import copy, deepcopy

import pymongo
from pymongo import MongoClient


class DAO_db_users(DAO):
    """
        DAO for accessing users related data in MongoDB
        Contains basics CRUD operaions
    """

    def __init__(self, MONGO_HOST="localhost", MONGO_PORT=27018, MONGO_USER="", MONGO_PASS="", MONGO_DB="spiceComMod"):
        """
        :Parameters:
            MONGO_HOST: mongodb address, Default value: "localhost"
            MONGO_PORT: mongodb port, Default value: 27018
            MONGO_USER: mongodb user, Default value: ""
            MONGO_PASS: mongodb pass, Default value: ""
            MONGO_DB: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__(MONGO_HOST)
        # print("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))
        uri = "mongodb://{}:{}@{}:{}/?authMechanism=DEFAULT&authSource=spiceComMod".format(MONGO_USER, MONGO_PASS,
                                                                                           MONGO_HOST, MONGO_PORT)
        self.mongo = MongoClient(uri)
        # self.mongo = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password)) #MongoClient("mongodb://{}:{}@{}:{}/".format(username, password, self.route, port))

        self.db_users = self.mongo.spiceComMod.users
        self.template = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx"
        }
        self.templateFull = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx",
            "source": "xxx",  # Not required
            "pname": "xxx",
            "pvalue": "xxx",
            "context": "xxx",  # Not required
            "datapoints": "xxx"  # Not required
        }
        self.templateWithoutP = {
            "id": "xxx",
            "userid": "xxx",
            "origin": "xxx",
            "source_id": "xxx",
            "source": "xxx",  # Not required
            "context": "xxx",  # Not required
            "datapoints": "xxx"  # Not required
        }

    def getData(self):
        return self.getUsers()

    def insertUser(self, userJSON):
        """
        Inserts user or list of users
        :Parameters:
            userJSON: JSON value, Type: json <class 'dict'> OR List(<class 'dict'>)
        """
        if type(userJSON) is list:
            self.__insertMany(userJSON)
        else:
            self.__insertOne(userJSON)

    def __insertOne(self, userJSON):
        """
            For every value that the user has, it inserts one document with that value as pname and pvalue
        """
        user = copy(userJSON)
        userTemplate = copy(self.template)
        # anadimos los campos necesarios
        # si es un id (viene del ugc) entonces lo guardamos
        # si es un _id (viene de mongodb) entonces lo ignoramos
        for key in user.keys():
            if key in self.template.keys():
                if key == "id":
                    userTemplate["id"] = user[key]
                elif key != "_id":
                    userTemplate[key] = user[key]

        items = (user.keys() - self.template.keys())
        for item in items:
            userWithP = copy(userTemplate)
            userWithP["pname"] = item
            userWithP["pvalue"] = user[item]
            self.db_users.insert_one(userWithP)

    def __insertMany(self, usersJSON):
        for user in usersJSON:
            self.__insertOne(user)

    def insertUser_API(self, userJSON):
        """
        Used only in the http server API
        :Return:
            Update Result: True or False
        """
        try:
            for userD in userJSON:
                self.db_users.update_one({"userid": userD["userid"], "pname": userD["pname"]}, {"$set": userD},
                                         upsert=True)
            return True
        except:
            return False

    def getUsers(self):
        """
        :Return:
            List with all users, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_users.find({})
        dataList = loads(dumps(list(dataList)))
        listUsersId = []
        # guardamos los id's de los usuarios
        for i in dataList:
            if i["userid"] not in listUsersId:
                listUsersId.append(i["userid"])
        # recorremos esos id's y metemos uno por uno a la lista
        listUsers = []
        for i in listUsersId:
            listUsers.append(self.getUser(i))
        return listUsers

    def getUser(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        :Return:
            User, Type: json <class 'dict'>
        """
        # data = self.db_users.find({"userid": userId}, {"_id": 0})
        data = self.db_users.find({"userid": userId})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        else:
            user = self.template.copy()
            # campos obligatorios
            # user["_id"] = data[0]["_id"]
            user["userid"] = data[0]["userid"]
            user["origin"] = data[0]["origin"]
            user["source_id"] = data[0]["source_id"]
            # campos no obligatorios
            if "id" in data[0]:  # temporalmente lo puse aqui
                user["id"] = data[0]["id"]
            if "source" in data[0]:
                user["source"] = data[0]["source"]
            if "context" in data[0]:
                user["context"] = data[0]["context"]
            if "datapoints" in data[0]:
                user["datapoints"] = data[0]["datapoints"]
            # pname and pvalue
            for item in data:
                user[item["pname"]] = item["pvalue"]

        return user

    def updateUser(self, newJSON):
        """
        Updates old values and add new if necessary

        :Parameters:
            newJSON: User/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        newData = copy(newJSON)
        if isinstance(newData, list):
            if len(newData) > 1:
                self.__updateMany(newData)
            else:
                self.__updateOne(newData[0])
        else:
            self.__updateOne(newData)

    def __updateOne(self, newData):
        # self.db_users.update_one({ "userid": newData["userid"], "pname": newData["pname"] }, newData, upsert = True)
        user = self.getUser(newData["userid"])
        if user == {}:
            self.insertUser(user)
        else:
            for item in newData.keys():
                if item not in self.templateWithoutP.keys():
                    user[item] = newData[item]  # actualizamos los valores y anadimos nuevos si hay
            self.deleteUser(newData["userid"])
            self.insertUser(user)

    def __updateMany(self, newData):
        for user in newData:
            self.__updateOne(user)

    # # Realiza casi lo mismo que el update, solo que cambia completamente todos los valores, no solo los campos P
    def replaceUser(self, newJSON):
        """
        Replaces all values (deletes the old one and creates a new one)

        :Parameters:
            newJSON: User/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        newData = copy(newJSON)
        if isinstance(newData, list):
            if len(newData) > 1:
                self.__replaceUserMany(newData)
            else:
                self.__replaceUserOne(newData[0])
        else:
            self.__replaceUserOne(newData)

    def __replaceUserOne(self, newData):
        self.deleteUser(newData["userid"])
        self.insertUser(newData)

    def __replaceUserMany(self, newData):
        for user in newData:
            self.__replaceUserOne(user)

    def deleteUser(self, userId):
        """
        :Parameters:
            userId: User id, Type: <class 'str'>
        """
        response = self.db_users.delete_many({"userid": userId})

    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_users.delete_many({})

    def userToPostAPIFormat(self, userJSON):
        """
        Splits user json object into their attribute components
        according to the user model format

        Parameters
        ----------
        userJSON : json object encoding a citizen.
            
        """

        
        user = copy(userJSON)
        userTemplate = copy(self.template)
        # anadimos los campos necesarios
        # si es un id (viene del ugc) entonces lo guardamos con otro nombre
        # si es un _id (viene de mongodb) entonces lo ignoramos
        for key in user.keys():
            if key in self.template.keys():
                if key == "id":
                    userTemplate["ugc_id"] = user[key]
                elif key != "_id":
                    userTemplate[key] = user[key]

        items = (user.keys() - self.template.keys())
        usersAPI = []
        for item in items:
            userWithP = copy(userTemplate)
            userWithP["pname"] = item
            userWithP["pvalue"] = user[item]
            usersAPI.append(userWithP)
        
        return usersAPI


