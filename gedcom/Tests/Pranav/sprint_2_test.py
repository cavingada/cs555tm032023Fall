from gedcom.Features.sprint2 import check_less_than_150_years_old, check_birth_before_marriage
import unittest
from gedcom.gedcom_parse import get_gedcom_df
import os

class TestUS(unittest.TestCase):
    
    def setUp(self):
        cwd = os.getcwd()
        self.individuals, self.families = get_gedcom_df(f'{cwd}/gedcom/example.ged')
        self.errors = check_less_than_150_years_old(self.individuals)
        self.errors += check_birth_before_marriage(self.individuals, self.families)

    
    def test_too_old(self):
        self.assertEqual(self.errors[0], 'ERROR: INDIVIDUAL: US07: @I1@ is too old')
    
    def test_born_after_divorce(self):
        self.assertEqual(self.errors[1], 'ERROR: INDIVIDUAL: US08: @I6@ is born after the divorce of the parents')

    def test_born_before_marriage(self):
        self.assertEqual(self.errors[2], 'ERROR: INDIVIDUAL: US08: @I1@ is born before the marriage of the parents')
        

if __name__ == '__main__':
    unittest.main()