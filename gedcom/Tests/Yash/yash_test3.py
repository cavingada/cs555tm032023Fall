import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint3 import check_fewer_than_15_siblings, check_male_last_names

cwd = os.getcwd()

# US15: Fewer than 15 Siblings
class TestUnder15Siblings(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = check_fewer_than_15_siblings(families)
        
        # true errors
        trueErrors = []
        
        self.assertEqual(errors,trueErrors)
        
        
# US16: Male Last Names
class TestMaleLastNames(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = check_male_last_names(individuals, families)
        
        # true errors
        trueErrors = ["ERROR: FAMILY: US16: @F1@ has children with different last names"]
        
        self.assertEqual(errors,trueErrors)
        
if __name__ == '__main__':
    unittest.main()