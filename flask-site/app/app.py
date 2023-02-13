# app.py
from helpers import *
import random as rnd
from flask import Flask, jsonify, request, render_template
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():

    data = request.form
    model = data['model']
    rate = data['rate']
    type = data['type']
    confirmed_type = data['confirm']

    user_selection = model + '_' + rate + '_cr_' + type
    if(confirmed_type =='careless'):
        print('careless type check')
        qlist = []
        for a in range(1, 25):
            # qlist.append(rnd.randint(1, 5))
            qlist.append(1)
    else:
        qlist = [4, 4, 3, 4, 5, 5, 4, 5, 5, 5, 4,
                   4, 3, 4, 4, 4, 4, 5, 5, 4, 4, 4, 5, 5]

    json_input = JSONParser(qlist, user_selection)
    prediction = predictList(json_input)
    print(prediction)
    response = f"""
    <p id="cr-result">Model {model} determined the confirmed type {confirmed_type} to be {prediction}
    based on a careless rate of {rate} and a survey type of {type} </p>
    """

    return response


    # return render_template('index.html', prediction_text='Determined to be {}'.format(prediction))

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=5000)

