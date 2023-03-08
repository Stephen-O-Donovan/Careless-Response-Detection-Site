
import pandas as pd
import numpy as np

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
    
    """

    def __init__(self, rr_data, cr_data, cr_rate=10, survey_data_type="human"):

        self.rr_data = rr_data
        self.rr_data_formatted = self.__dataframeFormat("Regular")

        self.cr_data = cr_data
        self.cr_data_formatted = self.__dataframeFormat("Careless")

        self.cr_rate = cr_rate
        self.survey_data = survey_data_type
        self.name = self.survey_data + "_" + str(self.cr_rate)

    def __dataframeFormat(self, responder_type):

        """
        Verifies the passed in data is in the correct format and returns the data
        with a column indicating careless condition.

        Raises execptions indicating format errors.

        """

        if responder_type == "Regular":
            dat = self.rr_data
        else:
            dat = self.cr_data

        if isinstance(dat, pd.DataFrame):
            if(len(dat.columns) != 24):
                raise Exception('%s responders data must be in a format of 24 columns, %i columns received' %(responder_type, len(dat.columns)))
            
            for col in dat.columns:
                if dat[col].dtype.kind not in ('i'):
                    raise Exception('%s responders data contains non-integer values' %(responder_type))
                
                if ( (all(np.where(dat[col] < 1, True, False)))):
                    raise Exception('%s responders data contains values smaller than 1' %(responder_type))
                if( (all(np.where(dat[col] > 5, True, False)) )):
                    raise Exception('%s responders data contains values greater than 5' %(responder_type))
        else:
            raise Exception('%s responders data is not in a data frame format' %(responder_type))
                
        #Rename all column to 1-24
        dat.columns = [str(i) for i in range(1, len(dat.columns)+1) ]

        #Append Careless column indicating if regualr or careless responder
        if responder_type == "Regular":
            dat["Careless"] = 0
        else:
            dat["Careless"] = 1

        return dat
