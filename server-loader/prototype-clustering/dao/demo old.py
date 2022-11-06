
"""
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
    route = r"test/data/annotated-stories.json"
    # route = r"test/data/generated.json"
    data = DAO_json(route).getData()


    # x = requests.post("http://localhost:8090/postData", json = data)
    x = requests.post("http://localhost:8080/v1.1/dataInput", json = data)
    print(x.text)
    
    
    # Starts user feedback
    
    # add perspective
    # Perspective (user attributes, artworks similarity features, emotion similarity on plutchik emotions similar artworks)
    filename = 'GAM similar user sentiment in similar artworks (iconclass) annotated-stories'
    with open('test/perspectives/' + filename + '.json', 'r', encoding='utf8') as f:
        perspective = json.load(f)[0]

    api = DAO_api()
    x = api.addPerspective(perspective)
    """
    """

    
   
    
    """
    """

main()

"""