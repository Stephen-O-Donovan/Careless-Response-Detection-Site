import json
import pandas as pd
# import requests
import sklearn.externals
import joblib
import imblearn
from boto.s3.key import Key
from boto.s3.connection import S3Connection

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = 'careless-detection-models'
MODEL_FILE_NAME_DEFAULT = 'gbm_10_cr_all.pkl'
MODEL_LOCAL_PATH_DEFAULT = '/tmp/' + MODEL_FILE_NAME_DEFAULT


def load_model(model_name):
    try:
        conn = S3Connection()
        bucket = conn.get_bucket(BUCKET_NAME)
        key_obj = Key(bucket)

        model_file = model_name + '.pkl'
        temp_model_path = ''
        try:
            key_obj.key = model_file
            temp_model_path = '/tmp/' + model_file
        except:
            print('could not find model, loading default')
            key_obj.key = MODEL_FILE_NAME_DEFAULT
            temp_model_path = '/tmp/' + MODEL_FILE_NAME_DEFAULT

        contents = key_obj.get_contents_to_filename(temp_model_path)
        model = joblib.load(temp_model_path)

    except:
        return '*** ERROR: COULD NOT LOAD MODEL ***'
    return model


def testDfCreate(lst):
    df = pd.DataFrame()
    for i in range(1, 25):
        df['Q' + str(i)] = 1
    df.loc[len(df)] = lst
    return df


def lambda_handler(event, context):

    # # Get input JSON data and convert it to a DF
    body = event.get('body')
    input_json = json.loads(body).get('input')
    model_name = json.loads(body).get('model')
    input_df = pd.DataFrame(input_json)
    result = {'output': []}
    list_out = []
    classifier = load_model(model_name)
    for i in range(len(input_df)):
        df = testDfCreate(input_df.iloc[i]['responder'])
        prediction = classifier.predict(df)
        list_out.append(prediction[0])

    predictions = list(map(lambda x: 'Careless' if x ==
                       1 else 'Regular', list_out))
    result['output'] = predictions
    result = json.dumps(result)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': result
    }
