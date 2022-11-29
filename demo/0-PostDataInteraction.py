

import requests
import json

def main():

    route1 = r"./data/new-annotated-stories.json"
    # route2 = r"test/data/parser_output.json"
    route2 = r"./data/GAM similar user emotions in similar artworks (iconclass) annotated-stories.json"

    with open(route1, 'r', encoding='utf8') as f:
        annotatedStories = json.load(f)
    with open(route2, 'r', encoding='utf8') as f:
        perspective = json.load(f)

    # api = DAO_api()

    a = requests.post("http://localhost:8080/v1.1/dataInput", json = annotatedStories)
    print(a)
    print(a.text)

    # b = requests.post("http://localhost:8080/v1.1/perspective", json = perspective)
    # print(b)
    # print(b.text)

main()