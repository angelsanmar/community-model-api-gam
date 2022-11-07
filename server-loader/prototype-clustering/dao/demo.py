from context import dao
from dao_class import DAO
import os

from context import dao
from dao.dao_class import DAO
from dao.dao_db_users import DAO_db_users
from dao.dao_db_communities import DAO_db_community
from dao.dao_db_similarities import DAO_db_similarity
from dao.dao_csv import DAO_csv
from dao.dao_json import DAO_json
from dao.dao_api import DAO_api
from dao.dao_linkedDataHub import DAO_linkedDataHub

import json

import requests
from requests.auth import HTTPBasicAuth

from bson.json_util import dumps, loads

# Daos
from dao.dao_db_interactionData import DAO_db_interactionDatas

from os import listdir
from os.path import isfile, join


def main():
    # api = DAO_api()

    route1 = r"../communityModel/data/new-annotated-stories.json"
    route2 = r"test/data/parser_output.json"
    route2 = r"../communityModel/perspectives/GAM similar user sentiments in similar artworks (iconclass) annotated-stories.json"
    annotatedStories = DAO_json(route1).getData()
    perspective = DAO_json(route2).getData()

    path = r"../communityModel/perspectives/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    # print(onlyfiles)

    initReq = requests.post("http://localhost:8080/v1.1/dataInput", json=annotatedStories)
    print(initReq)
    print(initReq.status_code)
    print(initReq.text)


    #### modo manual
    # initReq = requests.post("http://localhost:8080/v1.1/perspective", json=perspective)
    # print(initReq)
    # print(initReq.status_code)
    # print(initReq.text)

    #### modo iterativo
    i = 0
    for perspectiveFilename in onlyfiles:
        i = i + 1
        if any([att_name for att_name in ["Size_height", "Size_width", "Artwork_start_date"] if att_name in perspectiveFilename]):
            print("El fichero '", perspectiveFilename, "' se salto ya que daba errores por el formato de los datos")
            continue

        print("File: [", i, "of", len(onlyfiles), "]")
        try:
            perspective = DAO_json(path + perspectiveFilename).getData()
            res = requests.post("http://localhost:8080/v1.1/perspective", json=perspective)
        except:
            print("_Error occurred_")
            print("Filename: ", perspectiveFilename)
            break


main()
