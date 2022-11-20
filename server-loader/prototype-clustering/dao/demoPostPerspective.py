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



def main():
    route2 = r"../communityModel/perspectives/GAM similar user emotions in similar artworks (iconclass) annotated-stories.json"
    route2 = r"../communityModel/perspectives/GAM similar user emotions in similar artworks (artwork_artistic_movement) annotated-stories.json"
    perspective = DAO_json(route2).getData()

    b = requests.post("http://localhost:8080/v1.1/perspective", json = perspective)
    print(b)
    print(b.text)

main()