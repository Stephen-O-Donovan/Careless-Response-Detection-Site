
import unittest
import pandas as pd
import numpy as np

from careless_detection import Careless

df_template_valid = pd.DataFrame(columns=[i for i in range(24)])
df_template_invalid = pd.DataFrame(columns=[i for i in range(20)])

rr_data_valid = df_template_valid.copy()
for i in range (20):
    rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]

cr_data_valid = df_template_valid.copy()
for i in range (20):
    cr_data_valid.loc[len(cr_data_valid)] = [1 for i in range(24)]

rr_data_invalid = df_template_invalid.copy()
for i in range (20):
    rr_data_invalid.loc[len(rr_data_valid)] = [1 for i in range(20)]

cr_data_invalid = df_template_invalid.copy()
for i in range (20):
    cr_data_invalid.loc[len(cr_data_invalid)] = [1 for i in range(20)]

mainTester = Careless(rr_data_valid.copy(), cr_data_valid.copy())

class TestCareless(unittest.TestCase):

    def test_valid_dataframe(self):
        """
        Test that it can verify correctly formatted data
        """

        tester = Careless(rr_data_valid.copy(), cr_data_valid.copy())
        assert tester.name is not None

        # print(tester.rr_data_formatted)

    def test_valid_created_dataframe(self):
        """
        Test that it can correctly create the formatted dataframe
        """

        tester = Careless(rr_data_valid.copy(), cr_data_valid.copy())
        assert tester.name is not None

        self.assertEqual(len(tester.rr_data_formatted.columns), 25)
        self.assertEqual(len(tester.cr_data_formatted.columns), 25)

        self.assertEqual(list(tester.rr_data_formatted.columns)[-1], "Careless")
        self.assertEqual(list(tester.cr_data_formatted.columns)[-1], "Careless")

        self.assertEqual(tester.rr_data_formatted.iloc[0, -1], 0)
        self.assertEqual(tester.cr_data_formatted.iloc[0, -1], 1)

        # print(tester.rr_data_formatted)

    def test_invalid_dataframe(self):
        """
        Test that it can catch incorrectly formatted dataframes
        """


        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_invalid.copy())
        # print(str(context.exception))
        self.assertTrue('Careless responders data must be in a format of 24 columns, 20 columns received' in str(context.exception))

        rr_list = [1 for i in range (24)]
        with self.assertRaises(TypeError) as context:
            Careless(rr_list, cr_data_invalid)
        self.assertTrue('Regular responders data is not in a data frame format' in str(context.exception))

    def test_invalid_data_type(self):
        """
        Test that it can catch non-integer values 
        """

        cr_data_invalid_type = cr_data_valid.copy()
        cr_data_invalid_type.loc[0, 5] = 4.4

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_invalid_type)
        self.assertTrue('Careless responders data contains non-integer values' in str(context.exception))

    def test_NaN(self):
        """
        Test that it can catch NaN entries
        """

        cr_data_NaN = cr_data_valid.copy()
        cr_data_NaN.loc[0, 5] = np.nan

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_NaN)
        self.assertTrue('Careless responders data contains NaN entries' in str(context.exception))


    def test_invalid_data_range_large(self):
        """
        Test that it can catch data values greater than 6
        """

        cr_data_invalid_large = cr_data_valid.copy()
        cr_data_invalid_large.loc[0, 5] = int(7)

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_invalid_large)
        # print(str(context.exception))
        self.assertTrue('Careless responders data contains values greater than 6' in str(context.exception))

    def test_invalid_data_range_small(self):
        """
        Test that it can catch data values smaller than 1
        """

        cr_data_invalid_small = cr_data_valid.copy()
        cr_data_invalid_small.loc[0, 5] = int(0)

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_invalid_small)
        # print(str(context.exception))
        self.assertTrue('Careless responders data contains values smaller than 1' in str(context.exception))

    def test_cr_rate(self):
        """
        Test that it catches incorrectly supplied CR rate
        """

        tester = Careless(rr_data_valid.copy(), cr_data_valid.copy(), 20)
        assert tester.name is not None

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_valid.copy(), 51)
        self.assertTrue('CR rate must be an integer value between 1 and 50' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_valid.copy(), 0)
        self.assertTrue('CR rate must be an integer value between 1 and 50' in str(context.exception))

    def test_survey_data_type(self):
        """
        Test that it catches incorrectly supplied survey data type
        """

        tester = Careless(rr_data_valid.copy(), cr_data_valid.copy(), survey_data_type="all")
        self.assertEqual(tester.name, "all_10")

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_valid.copy(), survey_data_type='comp')
        self.assertTrue('Survey data type must be one of ["human", "computer", "all"]' in str(context.exception))

        with self.assertRaises(ValueError) as context:
            Careless(rr_data_valid.copy(), cr_data_valid.copy(), survey_data_type=0)
        self.assertTrue('Survey data type must be one of ["human", "computer", "all"]' in str(context.exception))

    def test_eval_before_fit(self):
        """
        Test that it catches trying to evaluate a model before building
        """
        tester = Careless(rr_data_valid.copy(), cr_data_valid.copy(), survey_data_type="all")
        with self.assertRaises(AttributeError) as context:
            tester.evaluate_model()
        self.assertTrue('Model must be build first, please run Careless.build_model()' in str(context.exception))

    def test_gbm_param_generator(self):
        """
        Test that it returns a parameter dictionary with the supplied arguements
        """

        param = mainTester.gbm_param_generator(300, learning_rate_step=0.4)
        print(param)
        print(param['n_estimators'])
        self.assertEqual(param['n_estimators'][0], 300)

        default_learning_rate_min = 0.5
        self.assertEqual(param['learning_rate'][2], default_learning_rate_min+(2*0.4))

    
if __name__ == '__main__':
    unittest.main()