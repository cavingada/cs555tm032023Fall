import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint4 import unique_name_and_birth_date, unique_families_by_spouses

# get df of families
cwd = os.getcwd()

# US17: No marriages to descendants
class TestUniqueNameAndBirthDate(unittest.TestCase):
    
    # test 1: 
    def test_unique_name_and_birth_date_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example8.ged'
        individuals, _ = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = unique_name_and_birth_date(individuals)

        # true errors 
        trueErrors = ['ERROR: US23: Name: Cavin /Gada/ and Birthday: 9 SEP 1872 are not unique']
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

# US18: siblings should not marry
class TestUniqueFamiliesBySpouses(unittest.TestCase):
    
    # test 1: 
    def test_unique_families_by_spouses_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example8.ged'
        _, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = unique_families_by_spouses(families)

        # true errors 
        trueErrors = ["ERROR: US24: Couple ('@I1@', '@I4@') is not unique", "ERROR: US24: Couple ('@I1@', '@I4@') is not unique"]
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

if __name__ == '__main__':
    unittest.main()