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
MODEL_FILE_NAME = 'gbm_10_cr_all.pkl'
MODEL_LOCAL_PATH = '/tmp/' + MODEL_FILE_NAME

def load_model():
    try:
        conn = S3Connection()
        bucket = conn.get_bucket(BUCKET_NAME)
        key_obj = Key(bucket)
        key_obj.key = MODEL_FILE_NAME

        contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
        model = joblib.load(MODEL_LOCAL_PATH)

    except:
        return 'fail'
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
    input_df = pd.DataFrame(input_json)
    result = {'output': []}
    list_out = []
    classifier = load_model()
    for i in range(len(input_df)):
        df = testDfCreate(input_df.iloc[i]['responder'])
        prediction = classifier.predict(df)
        list_out.append(prediction[0])

    predictions = list(map(lambda x: 'Careless' if x == 1 else 'Regular', list_out))
    result['output'] = predictions
    result = json.dumps(result)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': result
    }
