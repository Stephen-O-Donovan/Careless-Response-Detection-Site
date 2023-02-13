

import pickle
import pandas as pd
import requests
import json
from requests.auth import HTTPBasicAuth

AWS_URL = 'https://2gp1fuo9na.execute-api.eu-west-1.amazonaws.com/Prod/prediction/'

def JSONParser(lst, user_selection):

    dictionary = '''{"model":"''' + user_selection + \
        '''", "input":[{"responder":'''+str(lst)+'''}]}'''
    json_object = json.loads(dictionary)
    print(json_object)
    return json_object


def predictList(parsed_json):


    local_url = 'http://127.0.0.1:3000/prediction'
    auth = HTTPBasicAuth('apikey', '')
    res = requests.post(AWS_URL, json=parsed_json, auth=auth)
    print(res)
    body = res.json()
    if 'output' not in body:
        return ('There was an issue with this model')
    else:
        prediction = body['output']
        for p in prediction:
            if p == 'Regular':
                return ('A Regular Responder')
            else:
                return ('Carelessness Detected!')


def setType(model_select):

    switch = {
        'Gradient Boosted ': 'gbm',
        'K-Nearest Neighbours': 'knn',
        'Support Vector Machines': 'svm',
        'Neural Net': 'nnet'
    }
    return switch.get(model_select, "gbm")
