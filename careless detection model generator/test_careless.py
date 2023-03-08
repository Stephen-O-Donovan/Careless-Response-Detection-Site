
import unittest
import pandas as pd
from careless_detection import Careless

class TestCareless(unittest.TestCase):

    def test_valid_dataframe(self):
        """
        Test that it can verify correctly formatted data
        """

        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]
        # print('valid rr')
        # print(rr_data_valid)

        cr_data_valid = df_template_valid.copy()
        cr_data_valid.loc[len(cr_data_valid)] = [1 for i in range(24)]

        tester = Careless(rr_data_valid, cr_data_valid)
        assert tester.name is not None

        # print(tester.rr_data_formatted)

    def test_valid_created_dataframe(self):
        """
        Test that it can correctly create the formatted dataframe
        """

        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]
        # print('valid rr')
        # print(rr_data_valid)

        cr_data_valid = df_template_valid.copy()
        cr_data_valid.loc[len(cr_data_valid)] = [1 for i in range(24)]

        tester = Careless(rr_data_valid, cr_data_valid)
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
        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])
        df_template_invalid = pd.DataFrame(columns=[i for i in range(20)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]


        cr_data_invalid = df_template_invalid.copy()
        cr_data_invalid.loc[len(cr_data_invalid)] = [1 for i in range(20)]

        with self.assertRaises(Exception) as context:
            Careless(rr_data_valid, cr_data_invalid)
        self.assertTrue('Careless responders data must be in a format of 24 columns, 20 columns received' in str(context.exception))

        rr_list = [1 for i in range (24)]
        with self.assertRaises(Exception) as context:
            Careless(rr_list, cr_data_invalid)
        self.assertTrue('Regular responders data is not in a data frame format' in str(context.exception))

    def test_invalid_data_type(self):
        """
        Test that it can catch non-integer values 
        """

        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]

        cr_data_invalid = df_template_valid.copy()
        cr_data_invalid.loc[len(cr_data_invalid)] = [1 for i in range(24)]
        cr_data_invalid.loc[0, 5] = 4.4

        with self.assertRaises(Exception) as context:
            Careless(rr_data_valid, cr_data_invalid)
        self.assertTrue('Careless responders data contains non-integer values' in str(context.exception))


    def test_invalid_data_range_large(self):
        """
        Test that it can catch data values greater than 5
        """

        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]

        cr_data_invalid = df_template_valid.copy()
        cr_data_invalid.loc[len(cr_data_invalid)] = [1 for i in range(24)]
        cr_data_invalid.loc[0, 5] = int(6)
        # print(cr_data_invalid)

        with self.assertRaises(Exception) as context:
            Careless(rr_data_valid, cr_data_invalid)
        # print(str(context.exception))
        self.assertTrue('Careless responders data contains values greater than 5' in str(context.exception))

    def test_invalid_data_range_small(self):
        """
        Test that it can catch data values smaller than 1
        """

        df_template_valid = pd.DataFrame(columns=[i for i in range(24)])

        rr_data_valid = df_template_valid.copy()
        rr_data_valid.loc[len(rr_data_valid)] = [1 for i in range(24)]

        cr_data_invalid = df_template_valid.copy()
        cr_data_invalid.loc[len(cr_data_invalid)] = [1 for i in range(24)]
        cr_data_invalid.loc[0, 5] = int(0)
        # print(cr_data_invalid)

        with self.assertRaises(Exception) as context:
            Careless(rr_data_valid, cr_data_invalid)
        # print(str(context.exception))
        self.assertTrue('Careless responders data contains values smaller than 1' in str(context.exception))
    
if __name__ == '__main__':
    unittest.main()