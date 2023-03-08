# Careless Response Detection in survey data using Machine Learning

This is a central repository for all files related to building a website to test survey data and 
predict if it is filled out in a careless or thoughtless manner. This is based on the major thesis of my
Masters in Data Science, developed in R and recreated using Python.

## Project breakdown

This project is divided into three major sections; building and training the machine learning models, development of a 
backend framework to receive survey data from users and run the selected model, and a front end framework to allow
users to test the models.

### Building the models

Model building and training was done using R for my thesis project. This was recreated using Python. SKlearn was
used to develop all of the models except for BART which was instead built using R code imported into the Python 
project. Models were trained using 10-fold cross validation and evaluated based on Specificity, Sensitivity and AUROC.
The model types built were:

* K-Nearest Neighbours (KNN)
* Support Vector Machines (SVM)
* Neural Net (NNET)
* Random Forest (RF)
* Gradient Boosted Machines
* Bayesian Additive Regression Trees (BART)

For each model type, models were built based on one of three survey types (human generated, computer generated, and a mixture of both) and rate of expected careless responses (5, 10, 15 and 20%) for a total of 72 models. Each were
then pickled and saved. 
The folder careless detection model generator contains all the code, including a library to generate objects and unit testing code

### Building a backend framework

To allow users to test the models a backend framework was developed using AWS. Python code was created and set to run 
on an AWS Lambda service and connected to an AWS API Gateway point which served as the link between the frontend website and the models. This gateway receives the requests from the website and passes it on to the Lambda service. This then fetches and loads the selected model from an AWS S3 bucket, unpickles and runs it againes the survey data recieved, 
subsequently sending back its predictions on whether the survey data is considered careless. Development of the backend framework was done locally using the AWS CLI and AWS SAM.
Technologies used:

* AWS Lambda - to carry out code execution
* AWS SAM and AWS CLI - for local development
* AWS API Gateway - to link the end user website to the backend 
* S3 Buckets - To store the pickled models
* AWS Secrets Keeper - to allow S3Connection to securly access the S3 bucket

### Building a frontend website

Two versions of the end user website were developed, one using Python streamlit and the other using Python flask.
For both, docker was used to containerise the code and test development locally before uploading to an AWS ECR. 
AWS ECS was then used to deploy the webapp.
Technologies used

* Flask and streamlit - to build the webapp
* Docker - To create a virtual image ready to deploy to AWS
* AWS ECR and ECS - to store and deploy the docker image

### General development

The project was built on Windows but mainly used Windows Subsystem for Linux (WSL) and linux command tools. VSCode was used as an IDE due to it flexibility and ability to integrate WSL and Git directly. Git was used for version control.
Some other technologies used:

* HTMX - to allow asynchronous use of the webapp without need of AJAX, keeping the project mostly Python based
* Bootstrap - To structure and style the webapp
* Various shellscripts developed to shortcut certain tasks such as building and deploying the containerised image, and to insert sensitive credentials instead of having them hardcoded



