import unittest
import os
from gedcom.gedcom_parse import get_gedcom_df
from gedcom.Features.sprint3 import check_marriage_to_descendants, check_siblings_marry

# get df of families
cwd = os.getcwd()

# US17: No marriages to descendants
class TestMarriageToDescendents(unittest.TestCase):
    
    # test 1: 
    def test_marriage_to_descendents_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example6.ged'
        _, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_marriage_to_descendants(families)

        # true errors 
        trueErrors = ['ERROR: FAMILY: US17: @F4@ has a marriage to a descendant']
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

# US18: siblings should not marry
class TestSiblingsMarry(unittest.TestCase):
    
    # test 1: 
    def test_siblings_marry_works(self):
        example1 = f'{cwd}/gedcom/Tests/Cavin/Data/example7.ged'
        _, families = get_gedcom_df(example1)
        
        # get output of function to be tested
        errors = check_siblings_marry(families)

        # true errors 
        trueErrors = ['ERROR: FAMILY: US18: @I1@ and @I4@ are siblings and should not marry']
        
        # let's see if we are correct..
        self.assertEqual(errors,trueErrors)

if __name__ == '__main__':
    unittest.main()