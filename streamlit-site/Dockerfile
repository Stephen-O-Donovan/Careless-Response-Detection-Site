# base image
FROM ubuntu:22.04

# ubuntu installing - python, pip, graphviz
RUN apt-get update &&\
    apt-get install python3.9 -y &&\
    apt-get install python3-pip -y 

# exposing default port for streamlit
EXPOSE 8501

# making directory of app
WORKDIR /streamlit-docker

# copy over requirements
COPY requirements.txt ./requirements.txt

# install pip then packages
RUN pip3 install -r requirements.txt

# copying all files over
COPY . .

# cmd to launch app when container is run
CMD streamlit run Careless_Detection.py
