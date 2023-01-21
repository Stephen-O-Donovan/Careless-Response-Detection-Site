import streamlit as st

import numpy as np
import random as rnd
from helpers import *

st.set_page_config(
    page_title="Select Models",
    page_icon="",
)

st.write("Select from different models and settings")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.write('Select what kind of responders will be detected')
    cr_type = st.selectbox('Survey Type',options=['all', 'human', 'computer'])

with col2:
    st.write('Select the expected percentage rate of carelessness')
    cr_rate = str(st.selectbox('Careless Rate',options=[5, 10, 15, 20]))

with col3:
    st.write('Select the model type to use for detection')
    cr_model = setType(st.selectbox('Model', 
            options=['Random Forest', 'Gradient Boosted', 'K-Nearest Neighbours', 
            'Support Vector Machines', 'Neural Net']))

user_selection = cr_model + '_' + cr_rate + '_cr_' + cr_type

if st.button("Predict based on regular responder"):
    with st.spinner('Running ' + user_selection):
        rr_list = [4,4,3,4,5,5,4,5,5,5,4,4,3,4,4,4,4,5,5,4,4,4,5,5]
        # df = testDfCreate(rr_list)
        json_input = JSONParser(rr_list)
        predictList(json_input, user_selection)
    
    # predictDf(df, user_selection)

if st.button("Predict based on random generated surveys"):
    with st.spinner('Running ' + user_selection):
        cr_lst = []
        for a in range(1, 25):
            cr_lst.append(rnd.randint(1,5))

        json_input = JSONParser(cr_lst)
        predictList(json_input, user_selection)

if st.button("Score based on 100 random generated surveys"):
    score = 0
    with st.spinner('Running ' + user_selection):
        my_bar = st.progress(0)
        for run in range(100):
            my_bar.progress(run + 1)
            lst = []
            for a in range(1, 25):
                lst.append(rnd.randint(1,5))

            df = testDfCreate(lst)
            score += predictDf(df, user_selection, True)
    result = 'The model had a success rate of ' + str(score) + '%'
    if score < 50:
        st.error(result)
    elif score >= 50 and score < 80:
        st.warning(result)
    else:
        st.success(result)