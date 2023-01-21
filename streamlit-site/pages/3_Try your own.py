import streamlit as st
import pandas as pd
import numpy as np
import random as rnd
import pickle  
import time
from helpers import testDfCreate, predictDf

model = pickle.load(open('models/gbm_20_cr_all.pkl', 'rb'))

st.set_page_config(
    page_title="Try Your Own",
    page_icon="",
)

st.write("Take a survey and test if it is considered careless")

lst = []
placeholder = st.empty()
with placeholder.container():
    for i in range(1,25):
        lst.append(st.selectbox('Q'+str(i),options=[1,2,3,4,5], index=0, key=i+int(time.time()) ))
if st.button('Randomise Answers'):
    lst = []
    placeholder.empty()
    with st.spinner('Randomising...'):
        time.sleep(1)
    with placeholder.container():
        for i in range(1,25):
            lst.append(st.empty().selectbox('Q'+str(i),options=[1,2,3,4,5], index=rnd.randint(0,4), key=i+25+int(time.time())))
        # st.write(lst[i]) #.index=rnd.randint(0,4)
if st.button('Test Survey'):
    df = testDfCreate(lst)
    predictDf(df)