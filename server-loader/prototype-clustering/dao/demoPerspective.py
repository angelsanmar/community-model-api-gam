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



def main():
    
    filename = 'GAM similar user sentiments in similar artworks (iconclass) annotated-stories.json'
    route = r"test/perspectives/" + filename
    perspective = DAO_json(route).getData()

    x = requests.post("http://localhost:8080/v1.1/perspective", json = perspective)
    print(x)
    print(x.text)

main()
