import os
import pymongo
from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ForkingMixIn
from bson.objectid import ObjectId


import logging

from context import dao
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_db_perspectives import DAO_db_perspectives
from dao.dao_db_flags import DAO_db_flags
from dao.dao_db_interactionData import DAO_db_interactionDatas
from dao.dao_json import DAO_json
import time

from communityModel.communityModel import CommunityModel

server_loader_port = int(os.environ['CM_DOCKER_PORT'])
server_loader_ip = "0.0.0.0"

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_port = os.environ['DB_PORT']


class Handler(BaseHTTPRequestHandler):

    # TODO:
    # - incorrect path or filename
    # - create thread for each connection/request
    # - refactor code

    def do_GET(self):
        """
        _get handler_
        API doc:
        - GET:
        http://localhost:8090/file/all                                      -> return all files -- List
        http://localhost:8090/file/{fileId}                                 -> return the first file with name equal to "fileId" -- JSON
        http://localhost:8090/perspectives/all                              -> ... -- List
        http://localhost:8090/perspectives/{perspectiveId}                  -> ... -- JSON
        http://localhost:8090/perspectives/{perspectiveId}/communities      -> Communities with the same "perspectiveId" -- List
        http://localhost:8090/index                                         -> return json files index (returns only files id) -- list
        - POST:
        Used only for redirection of POST requests from API Spice and access DB from here
        """
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                     str(self.path), str(self.headers))
        try:
            request = self.path.split("/")
            print("Request GET: ", request)
            first_arg = request[1]
            if first_arg == "seed":
                self.__getSeed()
            elif first_arg == "perspectives":
                self.__getPerspertives(request)
            elif first_arg == "index":
                self.__getIndex()
            else:
                print("-Error-")
                self.__set_response(404)
                self.wfile.write(
                    "-Error-\nThis GET request is not defined.\nGET request for {}".format(self.path).encode('utf-8'))
        except Exception as e:
            print("-Error-")
            print(e)
            if str(e) != "pymongo.errors.ServerSelectionTimeoutError":
                self.__set_response(500)
                self.wfile.write(
                    "-Error-\nGET request for {}".format(self.path).encode('utf-8'))
                # raise
            else:
                self.__set_response(500)
                self.wfile.write(
                    "-MongoDB connection timeout error-\nGET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        """
        _post handler_

        """
        content_length = int(
            self.headers['Content-Length'])  # <--- Gets the size of data
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data)
        ok = False
        request = self.path.split("/")
        print("Request POST: ", request)
        first_arg = request[1]
        if first_arg == "perspective":
            perspectiveId = loads(post_data)
            print(perspectiveId)
            print("\n\n")

            # retrive perspective from db
            daoPerspective = DAO_db_perspectives()
            perspective = daoPerspective.getPerspective(
                ObjectId(perspectiveId))
            print("perspective: ", perspective)

            # retrive interactionData
            daoInteractionData = DAO_db_interactionDatas()
            interactionData = daoInteractionData.getInteractionData()["data"]

            # _CM_
            communityModel = CommunityModel(
                perspective, dao=daoInteractionData)
            communityModel.start()

            # Delete previous interaction data
            # daoInteractionData = DAO_db_interactionDatas()
            # daoInteractionData.drop()

            ok = True

            # remove perspective flag (user gets the persepectiveId)
            # daoFlags = DAO_db_flags()
            # daoFlags.deleteFlagById(perspectiveId)

        elif first_arg == "updateUsers":
            # add or update user
            users = loads(post_data)
            daoUsers = DAO_db_users()
            ok = daoUsers.insertUser_API(users)

        elif first_arg == "postData":
            ok = True
            # Se pasa el _id de interactionData en mongoDB
            dataId = loads(post_data)["dataId"]
            print("dataId: ", dataId)

            # Se obtiene el ultimo interactionData que fue pasado por la API
            # (Se usa busca el ultimo usando el _id pasado)
            # (en cualquier caso se puede omitir la busqiedad por id y simplemente pedir algun interactionData,
            # ya que voy a borrarlo despues de cada ejecucion del CM)
            daoInteractionData = DAO_db_interactionDatas()
            data = daoInteractionData.getInteractionDataById(ObjectId(dataId))[
                "data"]
            # print("data: ", data)

            # retrive perspective from db
            daoPerspective = DAO_db_perspectives()
            perspective = daoPerspective.getPerspectives()[0]
            # print("perspective: ", perspective)

            communityModel = CommunityModel(
                perspective, dao=daoInteractionData)
            communityModel.start()

            daoInteractionData.drop()

        elif first_arg == "update_CM":
            #data = loads(post_data.decode('utf-8'))
            data = "1000"
            print("update_CM")
            ok = "updateCM"

        # if ok == "updateCM":
        #     self.__set_response(204)
        #     self.wfile.write("POST request for {}".format(
        #         self.path).encode('utf-8'))
        #     # self.__updateCM(post_data)
        if ok != False:
            self.__set_response(204)
            self.wfile.write("POST request for {}".format(
                self.path).encode('utf-8'))
        else:
            self.__set_response(500)
            self.wfile.write("POST request for {}".format(
                self.path).encode('utf-8'))

    def __updateCM(self, post_data):
        # Check if there is an update flag
        daoPerspectives = DAO_db_perspectives()
        daoFlags = DAO_db_flags()

        flags = daoFlags.getFlags()
        for flag in flags:
            perspective = daoPerspectives.getPerspective(
                ObjectId(flag["perspectiveId"]))

            # Call to the community model
            communityModel = CommunityModel(perspective, flag)
            communityModel.start()

            # Remove flag
            daoFlags.deleteFlag(flag)

    def __set_response(self, code, dataType='text/html'):
        self.send_response(code)
        self.send_header('Content-type', dataType)
        self.end_headers()

    def __getSeed(self):
        # dao = DAO_db_community()
        data = {"test": "test"}
        self.__set_response(200, 'application/json')
        self.wfile.write(dumps(data).encode(encoding='utf_8'))


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(30)
        HTTPServer.finish_request(self, request, client_address)


def run(server_class=HTTPServer, handler_class=Handler):
    logging.basicConfig(level=logging.INFO)
    server_address = (server_loader_ip, server_loader_port)
    httpd = ForkingHTTPServer(server_address, handler_class)
    logging.info('Starting server-loader...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping server-loader...\n')


def removeData():
    daoP = DAO_db_perspectives()
    daoP.drop()
    daoC = DAO_db_community()
    daoC.drop()
    daoC.dropFullListAll()
    daoS = DAO_db_similarity()
    daoS.drop()
    daoF = DAO_db_flags()
    daoF.drop()
    daoID = DAO_db_interactionDatas()
    daoID.drop()
    daoU = DAO_db_users()
    daoU.drop()


def initData():

    # annotatedStories = DAO_json(
    #     "app/prototype-clustering/communityModel/data/new-annotated-stories.json").getData()
    # daoInteractionData = DAO_db_interactionDatas()
    # daoInteractionData.insertInteractionData({"data": annotatedStories})

    perspective = DAO_json(
        "app/prototype-clustering/communityModel/perspectives/GAM similar user emotions in similar artworks (iconclass) annotated-stories.json").getData()
    # print(perspective)
    daoPerspective = DAO_db_perspectives()
    daoPerspective.insertPerspective(perspective)

    # default data for Vis tests
    r = "app/prototype-clustering/api_server/data/"
    json1 = DAO_json(r + "S-emotions-S-artworks (country) agg.json").getData()
    json2 = DAO_json(r + "S-emotions-S-artworks (country) agg.json").getData()
    json3 = DAO_json(r + "S-emotions-S-artworks (iconclass) agg.json").getData()

    daoC = DAO_db_community()
    daoC.insertFileList(json1)
    daoC.insertFileList(json2)
    daoC.insertFileList(json3)

    # jsonAll = DAO_json("app/prototype-clustering/api_server/data/Allperspectives.json").getData()
    # daoP = DAO_db_perspectives()
    # daoP.insertPerspective(jsonAll)


if __name__ == '__main__':
    from sys import argv

    removeData()
    initData()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
