
"""
A comprehensive library to build various types of machine 
learning models aimed at detecting careless responses in 
survey data.

This library accepts, checks and formats survey data and allows
fitting of various types of ML models.

Testing and evaluation of the models is provided along with the
option to save fitted models as pickled files.

"""

import pandas as pd
import numpy as np
import random as rnd
import pickle
import time

# machine learning
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from imblearn.pipeline import Pipeline, make_pipeline
from imblearn.over_sampling import SMOTE

from sklearn import metrics
from sklearn.metrics import roc_curve, roc_auc_score

MODEL_LIST = ["gbm", "rf", "bart", "knn", "svm", "nnet"]

class Careless:
    """
    Instantiate an object to detect careless responses in survey data

    :param rr_data: a list of regular responsers
    :type rr_data: dataframe

    :param cr_data: a list of careless responders
    :type cr_data: dataframe

    :param cr_rate: the rate of careless responders expected
    :type cr_rate: int (1-50, default 10)

    :param survey_data_type: identifies the composition of the survey date
                                - human - survey data from actual responders
                                - computer - survey data generated synthetically
                                - all - a mixture of human and computer generated
    :type survey_data_type: String ("human", "computer", "all", default "human")

    :raises ValueError: if the cr rate is not an integer between 1 and 50
    :raises ValueError: if the survey data type is not one of ["human", "computer", "all"]
    
    """

    def __init__(self, rr_data, cr_data, cr_rate=10, survey_data_type="human"):

        if( (not isinstance(cr_rate, int)) or cr_rate < 1 or cr_rate > 50):
            raise ValueError('CR rate must be an integer value between 1 and 50')
        self.cr_rate = cr_rate

        if((not isinstance(survey_data_type, str)) or survey_data_type not in ["human", "computer", "all"]):
            raise ValueError('Survey data type must be one of ["human", "computer", "all"]')
        self.survey_data_type = survey_data_type

        self.name = self.survey_data_type + "_" + str(self.cr_rate)

        self.rr_data = rr_data
        self.rr_data_formatted = self.__dataframeFormat("Regular")

        self.cr_data = cr_data
        self.cr_data_formatted = self.__dataframeFormat("Careless")

        self.X_train, self.X_test, self.y_train, self.y_test = self._create_data_split()

        
    def __dataframeFormat(self, responder_type:str):

        """
        Verifies the passed in data is in the correct format and returns the data
        with a column indicating careless condition.

        Raises execptions indicating format errors.

        :param responder_type: "Regular" or "Careless" denoting type of responder
        :type resonder_type: str

        :raises ValueError: if the dataframe is not 24 columns in length
        :raises ValueError: if the data contains NaN entries or entries other than 1-6
        :raises TypeError: if the data is not in a dataframe format

        :return data frame with formatted column names and careless indication column
        

        """

        if responder_type == "Regular":
            dat = self.rr_data
        else:
            dat = self.cr_data

        if isinstance(dat, pd.DataFrame):
            if(len(dat.columns) != 24):
                raise ValueError('%s responders data must be in a format of 24 columns, %i columns received' %(responder_type, len(dat.columns)))
            if(dat.isnull().values.any()):
                raise ValueError('%s responders data contains NaN entries' % responder_type)
            
            for col in dat.columns:
                if dat[col].dtype.kind not in ('i'):
                    raise ValueError('%s responders data contains non-integer values' %(responder_type))
                
                if ( (dat[col] < 1 ).any()):
                    raise ValueError('%s responders data contains values smaller than 1' %(responder_type))
                if( (dat[col] > 6 ).any()):
                    raise ValueError('%s responders data contains values greater than 6' %(responder_type))
        else:
            raise TypeError('%s responders data is not in a data frame format' %(responder_type))
                
        #Rename all column to 1-24
        dat.columns = [str(i) for i in range(1, len(dat.columns)+1) ]

        #Append Careless column indicating if regular or careless responder
        if responder_type == "Regular":
            dat["Careless"] = 0
        else:
            dat["Careless"] = 1

        return dat
    
    def _create_data_split(self):
        """
        Creates a 70/30 training/testing split of the data for the models

        """

        rr_rate = (1- (self.cr_rate/100))
        cr_sample_num = int((self.rr_data_formatted.shape[0]/rr_rate)-self.rr_data_formatted.shape[0])
        cr_sample = self.cr_data_formatted.sample(n=cr_sample_num, replace=True)
        merged_data=pd.concat([self.rr_data_formatted,cr_sample],axis=0)
        merged_data= merged_data.sample(frac=1) 
        y = merged_data["Careless"]
        X = merged_data.drop("Careless", axis=1)

        return train_test_split(X,y,test_size=0.3,shuffle=True)
    
    def build_model(self, model="gbm", params={}):
        """
        Create a machine learning model based on passed in type of model and optional parameters

        :param model: The type of machine learning model to build
                        - "gbm" - Gradient Boosted Machine (defualt)
                        - "rf" - Random Forest
                        - "bart" - Bayesian Additive Regression Trees
                        - "knn" - K-Nearest Neighbours
                        - "svm" - Support Vector Machines
                        - "nnet" - Neural Net
        :type model: str

        :param params: optional list of parameters when building the model
        :type params: dictionary

        :raises ValueError: if the model is not a string or contained in the model list

        """

        if((not isinstance(model, str)) or model not in MODEL_LIST):
            raise ValueError('model must be one of' +  str(MODEL_LIST))
        
        self.model = model

        if(self.model == "gbm"):
            start = time.time()
            print("------------Building a %s model------------" % self.model)
            self.fitted_model = self._buildGBM(params)
            end = time.time()
            print("------------Finished building %s model------------" % self.model)
            print("------------Time taken: %f------------" % (end-start))
        
        if(self.model == "rf"):
            start = time.time()
            print("------------Building a %s model------------" % self.model)
            self.fitted_model = self._buildRF(params)
            end = time.time()
            print("------------Finished building %s model------------" % self.model)
            print("------------Time taken: %f------------" % (end-start))

    def evaluate_model(self, output=True):
        """
        Evaluates the fitted model. 
        Stores the calculated values of True Positive Rate (tpr), False Positive Rate (fpr),
        threshold, AUROC and confusion matrix in the object

        :param output: If True, prints the calculated values of tpr, fpr and 
         AUROC rounded to 2 decimal places, prints the thresholds and the 
          confusion matrix (default True)

        :raises AttributeError: if attempting to run before a model is fitted
        
        """
        if not hasattr( self, 'fitted_model' ):
            raise AttributeError("Model must be build first, please run Careless.build_model()")
        
        y_pred=pd.DataFrame((self.fitted_model.predict(self.X_test)))
        y_pred[y_pred >= 0.5] = 1
        y_pred[y_pred < 0.5] = 0

        self.fpr, self.tpr, self.thresholds = roc_curve(self.y_test, y_pred)
        self.AUROC = np.round(roc_auc_score(self.y_test, y_pred), 2)
        self.confusion_matrix = metrics.confusion_matrix(self.y_test, y_pred)

        if(output):

            print("false positive rate - ",round(self.fpr[1],2))
            print("true positive rate - ",round(self.tpr[1],2))
            print("thresholds - ",self.thresholds)
            print("AUROC - ",round(self.AUROC,2))
            print("confusion_matrix")
            print(self.confusion_matrix)

    def save_model(self, path=""):
        
        """
        Pickles the fitted model and saves it to the provided path.
        If no path provided save in current directory

        :param path: path to directory where the model is to be saved (default current directory)

        :raises AttributeError: if attempting to save before a model is fitted

        """

        if not hasattr( self, 'fitted_model' ):
            raise AttributeError("Model must be build first, please run Careless.build_model()")

        filename = path +  self.name + '_' + self.model + '.pkl'

        with open(filename, 'wb') as f:
            pickle.dump(self.fitted_model, f)

        print("Saved pickled model to " + filename)

    def gbm_param_generator(self, n_estimators_min=200, n_estimators_max=500, learning_rate_min=0.5, learning_rate_max=2.0, 
                            learning_rate_step=0.5, max_depth_min=8, max_depth_max=16,
                            subsample_min=0.7, subsample_max=1.0, subsample_step=0.1):
        
        """
        Generates a dictionary of parameters used for fitting a 
        Gradient Boosted Machine model

        """

        params = {"n_estimators": [n_estimators_min, n_estimators_max],
                  "learning_rate": np.arange(learning_rate_min, learning_rate_max, learning_rate_step), 
                  "max_depth": [i for i in range(max_depth_min, max_depth_max+1, 2)], 
                  "subsample": np.arange(subsample_min, subsample_max, subsample_step)}
        
        return params

    def _buildGBM(self, params):

        if('n_estimators' in params):
            n_estimators = params['n_estimators']
        else:
            n_estimators = [200, 500]

        if('learning_rate' in params):
            learning_rate = params.get('learning_rate')
        else:
            learning_rate = np.arange(0.5,2.0,0.5)

        if('max_depth' in params):
            max_depth = params.get('n_estimators')
        else:
            max_depth = [200, 500]

        if('subsample' in params):
            subsample = params['subsample']
        else:
            subsample = np.arange(0.7,1.0,0.1)

        # n_estimators = params.get('n_estimators') or [200, 500]
        # learning_rate = params.get('learning_rate').any() or np.arange(0.5,2.0,0.5)
        # max_depth = params.get('max_depth') or [8,10,12,14,16]
        # subsample = params.get('subsample') or np.arange(0.7,1.0,0.1)

        param_prefix = 'GradientBoostingClassifier'.lower()+('__')
        new_params = { 
            param_prefix+'n_estimators': n_estimators,
            param_prefix+'learning_rate': learning_rate,
            param_prefix+'max_depth' : max_depth,
            param_prefix+'subsample' : subsample
        }
        print("Building a Gradient Boosted Machine model. \nParameters:\nn_estimators:\t%s\nlearning_rate:\t%s\nmax_depth:\t%s\nsubsample:\t%s\n" 
              % (str(n_estimators), str(learning_rate), str(max_depth), str(subsample)))
        imba_pipeline = make_pipeline(SMOTE(random_state=1132), GradientBoostingClassifier(random_state=1132))
        grid_imba = GridSearchCV(imba_pipeline, param_grid=new_params, cv=10, scoring='recall',
                            return_train_score=True)
        return grid_imba.fit(self.X_train, self.y_train)
    
    def _buildRF(self, params):

        n_estimators = params.get('n_estimators') or [200, 500]
        max_features = params.get('max_features') or ['sqrt', 'log2']
        max_depth = params.get('max_depth') or [8,10,12,14,16]
        criterion = params.get('criterion') or ['gini', 'entropy']

        param_prefix = 'RandomForestClassifier'.lower()+('__')
        new_params = { 
            param_prefix+'n_estimators': n_estimators,
            param_prefix+'max_features': max_features,
            param_prefix+'max_depth' : max_depth,
            param_prefix+'criterion' : criterion
        }
        print("Building a Random Forest model. \nParameters:\nn_estimators:\t%s\nmax_features:\t%s\nmax_depth:\t%s\ncriterion:\t%s\n" 
              % (str(n_estimators), str(max_features), str(max_depth), str(criterion)))
        imba_pipeline = make_pipeline(SMOTE(random_state=1132), RandomForestClassifier(random_state=1132))
        grid_imba = GridSearchCV(imba_pipeline, param_grid=new_params, cv=10, scoring='recall',
                            return_train_score=True)
        return grid_imba.fit(self.X_train, self.y_train)

