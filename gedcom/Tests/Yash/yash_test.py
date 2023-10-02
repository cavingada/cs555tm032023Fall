import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint1 import check_birth_before_death

# get df of families
cwd = os.getcwd()

# US03: Birth before death Tests
class TestBirthBeforeDeath(unittest.TestCase):
    
    #test 1: check that birth before death returns empty list for no errors
    def test_birth_before_death_no_error(self):
        example1 = f'{cwd}/gedcom/Tests/Yash/Data/example1.ged'
        individuals, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_birth_before_death(individuals)

        # true errors 
        trueErrors = []

        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
    
    #test 2: check that birth before death returns error for birth after death
    def test_birth_before_death_basic_error(self):
        example2 = f'{cwd}/gedcom/Tests/Yash/Data/example2.ged'
        individuals, families = get_gedcom_df(example2)
        
        # get output of function to be tested
        errors = check_birth_before_death(individuals)
        
        # true errors
        trueErrors = ["ERROR: INDIVIDUAL: US03: @I1@: Died on 1 SEP 2019 before born on 9 SEP 2020"]
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
        
    #test 3: check that birth before death returns no error for birth on death (same day)
    def test_birth_before_death_same_day(self):
        example3 = f'{cwd}/gedcom/Tests/Yash/Data/example3.ged'
        individuals, families = get_gedcom_df(example3)
        
        # get output of function to be tested
        errors = check_birth_before_death(individuals)
        
        # true errors
        trueErrors = []
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
        
    #test 4: check that error is thrown for invalid dates
    def test_date_invalid(self):
        example4 = f'{cwd}/gedcom/Tests/Yash/Data/example4.ged'
        individuals, families = get_gedcom_df(example4)

        # check if exception is raised
        with self.assertRaises(Exception) as exception:
            check_birth_before_death(individuals)

        # Check if the exception message matches the true exception message
        self.assertEqual(str(exception.exception), "Invalid date format")
        
    #test 5: check multiple errors for birth after death
    def test_multiple_birth_after_death(self):
        example5 = f'{cwd}/gedcom/Tests/Yash/Data/example5.ged'
        individuals, families = get_gedcom_df(example5)
        
        # get output of function to be tested
        errors = check_birth_before_death(individuals)
        
        # true errors
        trueErrors = ["ERROR: INDIVIDUAL: US03: @I1@: Died on 9 SEP 1950 before born on 9 SEP 2020", "ERROR: INDIVIDUAL: US03: @I4@: Died on 2 APR 2012 before born on 7 MAR 2022"]
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
        
if __name__ == '__main__':
    unittest.main()