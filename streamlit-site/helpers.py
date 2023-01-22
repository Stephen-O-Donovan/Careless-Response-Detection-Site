
import streamlit as st
import pickle
import pandas as pd
import requests
import json
from requests.auth import HTTPBasicAuth

AWS_URL = 'https://ii7zuwwoapjvl5qbf5cajvyhfm0nqmex.lambda-url.eu-west-1.on.aws'


# @st.cache
# def testDfCreate(lst):
#     df = pd.DataFrame()
#     for i in range(1, 25):
#         df['Q' + str(i)] = 1
#     df.loc[len(df)] = lst
#     return df


# def predictDf(df, user_selection, scoring=False):
#     file = 'models/' + user_selection + '.pkl'
#     model = pickle.load(open(file, 'rb'))
#     prediction = model.predict(df)
#     if scoring:
#         return prediction[0]
#     if prediction[0] == 0:
#         st.success("A regular responder!")
#         st.balloons()
#     else:
#         st.warning("Carelessness detected!")


def JSONParser(lst, user_selection):
    # st.write('selection: ' + user_selection)
    # st.write(lst)
    dictionary = '''{"model":"''' + user_selection + \
        '''", "input":[{"responder":'''+str(lst)+'''}]}'''
    json_object = json.loads(dictionary)
    return json_object


def predictList(parsed_json):

    # url = LAMBDA_URL+'/invocations/123'
    url = 'http://127.0.0.1:3000/prediction'
    auth = HTTPBasicAuth('apikey', '')
    res = requests.post(url, json=parsed_json, auth=auth)
    body = res.json()
    if 'output' not in body:
        st.error('There was an issue with this model')
    else:
        prediction = body['output']
        for p in prediction:
            if p == 'Regular':
                st.success('A Regular Responder')
            else:
                st.error('Carelessness Detected!')


@st.cache
def setType(model_select):

    switch = {
        'Gradient Boosted ': 'gbm',
        'Random Forest': 'rf',
        'K-Nearest Neighbours': 'knn',
        'Support Vector Machines': 'svm',
        'Neural Net': 'nnet'
    }
    return switch.get(model_select, "gbm")
