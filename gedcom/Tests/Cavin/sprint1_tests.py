import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint1 import check_marriage_before_death

# get df of families
cwd = os.getcwd()

# US05: Marriage before death Tests
class TestMarriageBeforeDeath(unittest.TestCase):
    
    # test 1: 
    def test_marriage_after_death_returns_error(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example1.ged'
        individuals, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_marriage_before_death(individuals, families)

        # true errors 
        trueErrors = ["ERROR: FAMILY: US05: @F1@: Married on 10 MAY 2020 after husband's (@I1@) death on 1 SEP 1953", "ERROR: FAMILY: US05: @F2@: Married on 1 JAN 2018 after husband's (@I1@) death on 1 SEP 1953"]
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

    # test 2:
    def test_marriage_before_death_returns_empty_list(self):
        example2 = f'{cwd}/gedcom/Tests/Cavin/Data/example2.ged'
        individuals, families = get_gedcom_df(example2)
        
        # get output of function to be tested
        errors = check_marriage_before_death(individuals, families)

        # true errors 
        trueErrors = []

        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
        
    # test 3:
    def test_marriage_on_death_returns_empty_list(self):
        example3 = f'{cwd}/gedcom/Tests/Cavin/Data/example3.ged'
        individuals, families = get_gedcom_df(example3)
        
        # get output of function to be tested
        errors = check_marriage_before_death(individuals, families)

        # true errors 
        trueErrors = []

        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
    
    # test 4:
    def test_marriage_date_invalid(self):
        example3 = f'{cwd}/gedcom/Tests/Cavin/Data/example4.ged'
        individuals, families = get_gedcom_df(example3)

        # check if  exception is raised
        with self.assertRaises(Exception) as exception:
            check_marriage_before_death(individuals, families)

        # Check if the exception message matches the true exception message
        self.assertEqual(str(exception.exception), "Invalid date format")

    # test 5:
    def test_death_date_invalid(self):
        example3 = f'{cwd}/gedcom/Tests/Cavin/Data/example5.ged'
        individuals, families = get_gedcom_df(example3)

        # check if  exception is raised
        with self.assertRaises(Exception) as exception:
            check_marriage_before_death(individuals, families)

        # Check if the exception message matches the true exception message
        self.assertEqual(str(exception.exception), "Invalid date format")
    
if __name__ == '__main__':
    unittest.main()