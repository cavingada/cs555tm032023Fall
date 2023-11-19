import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint4 import correct_gender_for_role, unique_ids

cwd = os.getcwd()

# US21: Fewer than 15 Siblings
class TestGenderRoles(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = correct_gender_for_role(individuals, families)
        
        # true errors
        trueErrors = ['ERROR: US21: husband @I1@ is not male in family @F1@', 'ERROR: US21: husband @I1@ is not male in family @F2@']
        
        self.assertEqual(errors,trueErrors)
        
        
# US22: Male Last Names
class TestUniqueIds(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = unique_ids(individuals, families)
        
        # true errors
        trueErrors = []
        
        self.assertEqual(errors,trueErrors)
        
if __name__ == '__main__':
    unittest.main()