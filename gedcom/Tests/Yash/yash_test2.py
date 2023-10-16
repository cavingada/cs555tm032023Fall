import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint2 import check_birth_before_death_of_parents, check_marriage_after_14

cwd = os.getcwd()

# US09: Birth before death of parents
class TestBirthBeforeDeathofParents(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = check_birth_before_death_of_parents(individuals, families)
        
        # true errors
        trueErrors = ["ERROR: INDIVIDUAL: US09: @I6@ is born 9 months after the death of the father", "ERROR: INDIVIDUAL: US09: @I7@ is born 9 months after the death of the father"]
        
        self.assertEqual(errors,trueErrors)
        
        
# US10: Marriage after 14
class TestMarriageAfter14(unittest.TestCase):
    
    # test 1
    def test_working(self):
        example = f'{cwd}/gedcom/Tests/Yash/Data/example.ged'
        individuals, families = get_gedcom_df(example)
        
        # get output of function to be tested
        errors = check_marriage_after_14(individuals, families)
        
        # true errors
        trueErrors = ["ERROR: INDIVIDUAL: US10: @I2@ was married before 14"]
        
        self.assertEqual(errors,trueErrors)
        
if __name__ == '__main__':
    unittest.main()