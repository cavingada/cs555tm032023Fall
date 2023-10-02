from gedcom.Features.sprint1 import check_dates_before_current
import unittest
from gedcom.gedcom_parse import get_gedcom_df
import os

class TestUS01(unittest.TestCase):
    
    def setUp(self):
        cwd = os.getcwd()
        self.individuals, self.families = get_gedcom_df(f'{cwd}/gedcom/Tests/Pranav/us01_test.ged')
        self.errors = check_dates_before_current(self.individuals, self.families)

    
    def test_birth(self):
        self.assertEqual(self.errors[0], 'ERROR: INDIVIDUAL: US01: @I1@: Birthday 4 MAY 2050 occurs in the future')
    
    def test_death(self):
        self.assertEqual(self.errors[1], 'ERROR: INDIVIDUAL: US01: @I2@: Death 3 JUN 2060 occurs in the future')

    def test_marriage(self):
        self.assertEqual(self.errors[2], 'ERROR: FAMILY: US01: @F1@: Marriage 12 MAY 2080 occurs in the future')

    def test_divorce(self):
        self.assertEqual(self.errors[3], 'ERROR: FAMILY: US01: @F5@: Divorce 3 APR 2070 occurs in the future')
        
    def test_no_errors(self):
        cwd = os.getcwd()
        individuals, families = get_gedcom_df(f'{cwd}/gedcom/Tests/Pranav/us01_test_no_errors.ged')
        errors = check_dates_before_current(individuals, families)
        self.assertEqual(len(errors), 0)

if __name__ == '__main__':
    unittest.main()