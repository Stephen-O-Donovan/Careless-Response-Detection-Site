import streamlit as st
import pandas as pd
import numpy as np
import random as rnd
import pickle
import time
from helpers import *

st.set_page_config(
    page_title="Try Your Own",
    page_icon="",
)

st.write("Take a survey and test if it is considered careless")

lst = []
dict = {}
for i in range(1, 25):
    dict[i] = st.selectbox(
        'Q'+str(i), options=[1, 2, 3, 4, 5])

st.write("Select from different models and settings")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.write('Select what kind of responders will be detected')
    cr_type = st.selectbox('Survey Type', options=['all', 'human', 'computer'])

with col2:
    st.write('Select the expected percentage rate of carelessness')
    cr_rate = str(st.selectbox('Careless Rate', options=[5, 10, 15, 20]))

with col3:
    st.write('Select the model type to use for detection')
    cr_model = setType(st.selectbox('Model',
                                    options=['Random Forest', 'Gradient Boosted', 'K-Nearest Neighbours',
                                             'Support Vector Machines', 'Neural Net']))

user_selection = cr_model + '_' + cr_rate + '_cr_' + cr_type

if st.button('Test Survey'):
    lst = []
    for i in range(1, 25):
        lst.append(dict[i])
    with st.spinner('Running ' + user_selection):

        json_input = JSONParser(lst, user_selection)
        predictList(json_input)
