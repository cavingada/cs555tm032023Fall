import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint2 import check_bigamy, check_parents_too_old

# get df of families
cwd = os.getcwd()

# US11: No Bigamy
class TestBigamy(unittest.TestCase):
    
    # test 1: 
    def test_check_bigamy_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example1.ged'
        individuals, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_bigamy(individuals, families)

        # true errors 
        trueErrors = ['ERROR: INDIVIDUAL: US11: @I1@ is a bigamist']
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

# US12: Check Parents too old
class TestParentsTooOld(unittest.TestCase):
    
    # test 1: 
    def test_parents_too_old_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example1.ged'
        individuals, _ = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_parents_too_old(individuals)

        # true errors 
        trueErrors = ['ERROR: INDIVIDUAL: US12: @I1@ is a parent and is too old']
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)
    
if __name__ == '__main__':
    unittest.main()